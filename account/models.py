from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="ایمیل شما")
    ip_address = models.GenericIPAddressField(verbose_name="آدرس آیپی", null=True, blank=True)
    profile_image = models.ImageField(verbose_name="عکس پروفایل", null=True, blank=True)
    likes_count = models.PositiveBigIntegerField(verbose_name="تعداد پسند ها", null=True, blank=True)
    comments_count = models.PositiveBigIntegerField(verbose_name="تعداد کامنت ها", null=True, blank=True)
    posts_count = models.PositiveBigIntegerField(verbose_name="تعداد پست ها", null=True, blank=True)
    all_requests_count = models.PositiveBigIntegerField(verbose_name="تعداد کل درخواست ها", null=True, blank=True)
    requests_search_count = models.PositiveBigIntegerField(verbose_name="تعداد درخواست های جستجو", null=True, blank=True)
    requests_download_count = models.PositiveBigIntegerField(verbose_name="تعداد درخواست های دانلود کردن", null=True, blank=True)
    excessive_requests_count = models.PositiveBigIntegerField(verbose_name="تعداد درخواست های بیش از حد اندازه", null=True, blank=True)

    def __str__(self):
        return self.username