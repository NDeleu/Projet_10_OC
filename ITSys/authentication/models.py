from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(gettext_lazy('The Email must be set.'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        extra_fields.setdefault('is_active', True)

        user.save()
        user.user_id = user.pk
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(gettext_lazy('SuperUser must be a staff member.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(gettext_lazy('SuperUser must be a superuser'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(gettext_lazy('email adress'), unique=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    user_id = models.IntegerField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
