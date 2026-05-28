from celery import shared_task
from django.core.mail import send_mail
from .models import Event
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, autoretry_for=(Exception,), max_retries=3, retry_backoff=True)
def send_event_email(self, event_id):
    try:
        event = Event.objects.select_related('creator').get(pk=event_id)
    except Event.DoesNotExist:
        logger.warning(f"Event {event_id} not found. Task skipped.")
        return

    if event.email_task_id != self.request.id:
        logger.info(f"Task ID mismatch for event {event.title}. Skipping obsolete task.")
        return

    if event.email_sent:
        logger.info(f"Email already sent for event {event.title}.")
        return

    if not event.send_email:
        logger.info(f"Email sending disabled for event {event.title}.")
        return

    try:
        send_mail(
            subject=f"Event reminder: {event.title}",
            message=f"Your event '{event.title}' is coming up at {event.deadline}!",
            from_email="mahdi.ar1384.ir@gmail.com",
            recipient_list=[event.creator.email],
        )
        
        event.email_sent = True
        event.email_task_id = None
        event.save(update_fields=["email_sent", "email_task_id"])
        
    except Exception as exc:
        logger.error(f"Error sending email for event {event_id}: {exc}")
        raise self.retry(exc=exc)
