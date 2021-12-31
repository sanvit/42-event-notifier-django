from django.db import models
import uuid

from django.db.models.fields import related

# Create your models here.


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          null=False, blank=False, auto_created=True)
    ft_id = models.PositiveIntegerField(null=False, blank=False, unique=True)
    name = models.CharField(max_length=100, default='',
                            null=False, blank=False)
    description = models.CharField(
        max_length=500, default='', null=False, blank=False)
    location = models.CharField(
        max_length=100, default='', null=False, blank=False)
    kind = models.CharField(max_length=100, default='',
                            null=False, blank=False)
    max_people = models.IntegerField(null=True, blank=True)
    nbr_subscribers = models.IntegerField(default=0, null=False, blank=False)
    begin_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)
    campus = models.ForeignKey(
        'Campus', on_delete=models.CASCADE, related_name='events')
    cursus = models.ForeignKey(
        'Cursus', on_delete=models.CASCADE, related_name='events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ft_created_at = models.DateTimeField(default='', null=False, blank=False)
    ft_updated_at = models.DateTimeField(default='', null=False, blank=False)
    theme = models.ManyToManyField('Theme', related_name='events')


class Theme(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          null=False, blank=False, auto_created=True)
    ft_id = models.PositiveIntegerField(
        default=0, null=False, blank=False, unique=True)
    name = models.CharField(max_length=100, default='',
                            null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ft_created_at = models.DateTimeField(default='', null=False, blank=False)
    ft_updated_at = models.DateTimeField(default='', null=False, blank=False)


class Campus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          null=False, blank=False, auto_created=True)
    ft_id = models.PositiveIntegerField(
        null=False, blank=False, unique=True)
    name = models.CharField(max_length=100, default='',
                            null=False, blank=False)
    country = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')


class Cursus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          null=False, blank=False, auto_created=True)
    ft_id = models.PositiveIntegerField(
        null=False, blank=False, unique=True)
    name = models.CharField(max_length=100, default='',
                            null=False, blank=False)
    slug = models.CharField(max_length=100, default='',
                            null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    ft_created_at = models.DateTimeField(default='', null=False, blank=False)
