from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
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
        is_admin = input("Do you want user is admin? (y/n): ")

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if is_admin == "y":
            extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


def upload_location(instance, filename):
    extension = filename.split(".")[1]

    if extension != "jpg":
        raise ValidationError(f"شما می توانید فقط فایل هایی با پسوند jpg آپلود کنید.")

    return f"user_profiles/{instance.username.lower()}/{instance.username.lower()}.{extension}"

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="ایمیل شما")
    profile_image = models.ImageField(upload_to=upload_location, verbose_name="عکس پروفایل", null=True, blank=True)
    all_requests_count = models.PositiveBigIntegerField(verbose_name="تعداد کل درخواست ها", null=True, blank=True, default=0)
    requests_search_count = models.PositiveBigIntegerField(verbose_name="تعداد درخواست های جستجو", null=True, blank=True, default=0)
    requests_download_count = models.PositiveBigIntegerField(verbose_name="تعداد درخواست های دانلود کردن", null=True, blank=True, default=0)
    excessive_requests_count = models.PositiveBigIntegerField(verbose_name="تعداد درخواست های بیش از حد اندازه", null=True, blank=True, default=0)
    is_admin = models.BooleanField(default=False, verbose_name="ادمین سایت")
    
    objects = CustomUserManager()

    def __str__(self):
        return self.username

    @property
    def get_name_or_username(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        else:
            return self.username