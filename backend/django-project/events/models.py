from django.db import models
from user.models import CustomUser
from datetime import timedelta

class Category(models.Model):
    title = models.CharField(max_length=100)
    creator = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    

class Event(models.Model):
    title = models.CharField(max_length=100)
    creator = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(blank=False)
    send_email = models.BooleanField(default=True)
    when_send_email = models.PositiveIntegerField(default=24)
    email_sent = models.BooleanField(default=False)
    email_task_id = models.CharField(null=True, blank=True)

    @property
    def email_send_time(self):
        if not self.send_email or not self.when_send_email:
            return None
        return self.deadline - timedelta(hours=self.when_send_email)

    def __str__(self):
        return self.title
