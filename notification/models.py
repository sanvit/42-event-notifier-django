from django.db import models
from django.conf import settings
import uuid
# Create your models here.


class Email(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          null=False, blank=False, auto_created=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='noti_email', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.email}'


class SMS(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          null=False, blank=False, auto_created=True)
    number = models.CharField(max_length=20)
    country_code = models.CharField(max_length=10)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='noti_sms', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.phone_number}'


class Telegram(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          null=False, blank=False, auto_created=True)
    chat_id = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='noti_telegram', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
