from django.contrib.auth import get_user_model
from django.db import models
from extensions.timestamp import TimeStamp

from .main import Post

__all__ = ("Ip", "Hit", "UserHit", "Like", "Download") 

User = get_user_model()

class Ip(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="آدرس آیپی")
    last_excessive_request_time = models.DateTimeField(verbose_name="آخرین وقت درخواست غیر مجاز")
    excessive_requests_count = models.PositiveIntegerField(
    verbose_name="تعداد درخواست های بیش از حد اندازه", null=True, 
    blank=True, default=0)

    class Meta:
        verbose_name = "آیپی"
        verbose_name_plural = "آیپی ها"

    def __str__(self):
        return self.ip_address

class Hit(TimeStamp):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
    verbose_name="پست", related_name="hits")
    ip_address = models.ForeignKey(Ip, on_delete=models.CASCADE, 
    verbose_name="آدرس آیپی", related_name="hits")

    class Meta:
        verbose_name = "بازدید"
        verbose_name_plural = "بازدید ها"
        ordering = ("-created",)

class UserHit(TimeStamp):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
    verbose_name="پست", related_name="user_hits")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
    verbose_name="کاربر", related_name="hits")

    class Meta:
        verbose_name = "بازدید کاربر"
        verbose_name_plural = "بازدید کاربران"
        ordering = ("-created",)

class LikeManager(models.Manager):
    def active(self):
        return self.filter(status=True)

class Like(TimeStamp):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
    verbose_name="پست", related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
    verbose_name="کاربر", related_name="likes")
    status = models.BooleanField(default=False, verbose_name="وضعیت")

    objects = LikeManager()

    class Meta:
        verbose_name = "لایک"
        verbose_name_plural = "لایک ها"
        ordering = ("-created",)

class Download(TimeStamp):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
    verbose_name="پست", related_name="downloads")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
    verbose_name="کاربر", related_name="downloads")

    class Meta:
        verbose_name = "دانلود"
        verbose_name_plural  = "دانلود ها"
        ordering = ("-created",)
        