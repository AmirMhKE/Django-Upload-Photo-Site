from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django_jalali.db import models as jmodels
from extension.utils import get_random_str

from .validators import persian_name_validator, persian_text_validator


def upload_location(instance, filename):
    return f"user_profiles/{instance.username.lower()}/{get_random_str(10, 50)}.jpg"

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=20, validators=[persian_name_validator], 
    verbose_name="نام", blank=True)
    last_name = models.CharField(max_length=30, validators=[persian_name_validator], 
    verbose_name="نام خانوادگی", blank=True)
    email = models.EmailField(unique=True, verbose_name="ایمیل شما")
    date_joined = jmodels.jDateTimeField("تاریخ عضویت", default=timezone.now)
    profile_image = models.ImageField(upload_to=upload_location, verbose_name="عکس پروفایل", 
    null=True, blank=True)
    about_me = models.TextField(validators=[persian_text_validator], max_length=150, 
    verbose_name="درباره من", null=True, blank=True)
    all_requests_count = models.PositiveBigIntegerField(verbose_name="تعداد کل درخواست ها", 
    null=True, blank=True, default=0)
    requests_download_count = models.PositiveBigIntegerField(
    verbose_name="تعداد درخواست های دانلود کردن", null=True, blank=True, default=0)
    excessive_requests_count = models.PositiveBigIntegerField(
    verbose_name="تعداد درخواست های بیش از حد اندازه", null=True, blank=True, default=0)
    is_admin = models.BooleanField(default=False, verbose_name="ادمین سایت")

    def __str__(self):
        return self.username

    @property
    def get_name_or_username(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.username
