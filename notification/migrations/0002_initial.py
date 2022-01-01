# Generated by Django 3.2.10 on 2022-01-01 07:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegram',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='noti_telegram', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sms',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='noti_sms', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='email',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='noti_email', to=settings.AUTH_USER_MODEL),
        ),
    ]
