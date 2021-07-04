from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="ایمیل شما")
    profile_image = models.ImageField(verbose_name="عکس پروفایل", null=True, blank=True)
    all_requests_count = models.PositiveBigIntegerField(verbose_name="تعداد کل درخواست ها", null=True, blank=True, default=0)
    requests_search_count = models.PositiveBigIntegerField(verbose_name="تعداد درخواست های جستجو", null=True, blank=True, default=0)
    requests_download_count = models.PositiveBigIntegerField(verbose_name="تعداد درخواست های دانلود کردن", null=True, blank=True, default=0)
    excessive_requests_count = models.PositiveBigIntegerField(verbose_name="تعداد درخواست های بیش از حد اندازه", null=True, blank=True, default=0)

    def __str__(self):
        return self.username