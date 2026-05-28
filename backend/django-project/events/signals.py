from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver
from django.db import transaction
from celery import current_app
from .models import Event
from .tasks import send_event_email

@receiver(pre_delete, sender=Event)
def revoke_task_on_delete(sender, instance, **kwargs):
    if instance.email_task_id:
        current_app.control.revoke(instance.email_task_id, terminate=True)

@receiver(pre_save, sender=Event)
def check_changes_before_save(sender, instance, **kwargs):
    if not instance.pk:
        instance._is_new = True
        instance._schedule_changed = True
        instance._old_task_id = None
    else:
        instance._is_new = False
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            time_changed = old_instance.email_send_time != instance.email_send_time
            sending_status_changed = old_instance.send_email != instance.send_email
            
            instance._schedule_changed = time_changed or sending_status_changed
            instance._old_task_id = old_instance.email_task_id
        except sender.DoesNotExist:
            instance._schedule_changed = True
            instance._old_task_id = None

@receiver(post_save, sender=Event)
def handle_task_scheduling(sender, instance, created, update_fields, **kwargs):
    if update_fields and 'email_sent' in update_fields and len(update_fields) == 1:
        return

    if not getattr(instance, '_schedule_changed', False):
        return

    def manage_task():
        if hasattr(instance, '_old_task_id') and instance._old_task_id:
            current_app.control.revoke(instance._old_task_id, terminate=True)

        if not instance.send_email or instance.email_sent:
            if instance.email_task_id:
                Event.objects.filter(pk=instance.pk).update(email_task_id=None)
            return

        eta = instance.email_send_time
        if eta:
            result = send_event_email.apply_async(args=[instance.id], eta=eta)
            
            Event.objects.filter(pk=instance.pk).update(email_task_id=result.id)

    transaction.on_commit(manage_task)
