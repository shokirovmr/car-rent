from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.forAUTH.utils.validator import validate_uzbekistan_number
from apps.shared.models import AbstractBaseModel


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone number must be set')
        validate_uzbekistan_number(phone)
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
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
    phone = models.CharField(unique=True, max_length=13, validators=[validate_uzbekistan_number],
                             verbose_name="Telefon raqam")
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'



