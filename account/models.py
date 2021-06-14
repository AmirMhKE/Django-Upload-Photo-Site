from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            msg = "شما باید یک ایمیل ثبت کنید!"
            raise ValueError(msg)

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    ip_address = models.GenericIPAddressField(verbose_name="آدرس آیپی", null=True)
    profile_image = models.ImageField(verbose_name="عکس پروفایل", null=True)
    likes_count = models.PositiveBigIntegerField(verbose_name="تعداد پسند ها", null=True)
    comments_count = models.PositiveBigIntegerField(verbose_name="تعداد کامنت ها", null=True)
    posts_count = models.PositiveBigIntegerField(verbose_name="تعداد پست ها", null=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.username