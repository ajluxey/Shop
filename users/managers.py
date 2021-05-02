from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.auth.models import User


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name, phone, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email,
                          first_name=first_name,
                          last_name=last_name,
                          phone=phone,
                          **extra_fields)
        user.set_password(password)
        # client_group = Group.objects.get(name='Client')
        # user.groups.set(client_group)
        user.save()
        return user

    def create_superuser(self, email, password, first_name, last_name, phone, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, first_name, last_name, phone, **extra_fields)
