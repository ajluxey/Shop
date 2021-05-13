from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'
    first_name = models.CharField(max_length=128, db_index=True, verbose_name='Имя')
    last_name = models.CharField(max_length=128, db_index=True, verbose_name='Фамилия')
    phone = models.CharField(max_length=12, unique=True, verbose_name='Телефон')
    email = models.EmailField(unique=True, verbose_name='Почта')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']
    objects = CustomUserManager()

    def __str__(self):
        return self.first_name + ' ' + self.last_name