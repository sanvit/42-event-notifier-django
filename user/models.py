from core.models import Cursus, Campus
import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
# Create your models here.


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, username):
        user = self.model(username=username)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, ft_id, password):
        user = self.model(username=username)
        user.set_password(password)
        user.ft_id = ft_id
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    """
    [User Model]
    """

    objects = UserManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          null=False, blank=False, auto_created=True)
    ft_id = models.PositiveIntegerField(
        null=False, blank=False, unique=True)
    username = models.CharField(
        max_length=20, blank=False, null=False, unique=False)
    email = models.EmailField(max_length=255, null=True, blank=True)
    cursus = models.ManyToManyField(Cursus, related_name='user', blank=True)
    campus = models.ManyToManyField(Campus, related_name='user', blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "ft_id"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username}"
