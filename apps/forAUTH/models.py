from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from apps.forAUTH.utils.validator import validate_uzbekistan_number
from apps.shared.models import AbstractBaseModel


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone number must be set')
        user = self.model(phone=phone, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, password, **extra_fields)


class User(AbstractUser, AbstractBaseModel):
    fullname = models.CharField(max_length=255, null=True, blank=True, verbose_name="Ism-familiya")
    phone = models.CharField(unique=True, max_length=13, verbose_name="Telefon raqam")
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    REQUIRED_FIELDS = ['phone']
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        self.full_clean()  # This will call the clean method to perform validation
        if self.pk is None and self.password:
            self.set_password(self.password)
        super().save(*args, **kwargs)
