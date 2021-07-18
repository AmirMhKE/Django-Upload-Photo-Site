from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

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

    def __str__(self):
        return self.username

    @property
    def get_name_or_username(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        else:
            return self.username