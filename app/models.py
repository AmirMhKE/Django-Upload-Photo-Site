from comment.models import Comment
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.html import format_html

user = get_user_model()

class PostManager(models.Manager):
    def published(self):
        return self.filter(status="p")

class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)

class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="عنوان دسته بندی")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="آدرس دسته بندی")
    position = models.PositiveIntegerField(unique=True, verbose_name="مختصات")
    status = models.BooleanField(default=True, verbose_name="آیا نمایش داده شود؟")

    objects = CategoryManager()

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
        ordering = ["-status", "position"]

    def __str__(self):
        return self.title

class Ip(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="آدرس آیپی")

    class Meta:
        verbose_name = "آیپی"
        verbose_name_plural = "آیپی ها"

    def __str__(self):
        return self.ip_address

class Post(models.Model):
    STATUS_CHOICES = (
        ("p", "منتشر شده"),
        ("i", "در حال بررسی"),
        ("b", "برگشت داده شده"),
    )
    title = models.CharField(max_length=100, verbose_name="عنوان عکس")
    slug = models.CharField(max_length=250, unique=True, verbose_name="آدرس عکس")
    img = models.ImageField(upload_to="images", verbose_name="عکس شما")
    publisher = models.ForeignKey(user, on_delete=models.SET_NULL, null=True, verbose_name="منتشر کننده")
    category = models.ForeignKey(Category, verbose_name="دسته بندی", related_name="posts", on_delete=models.SET_NULL, null=True)
    hits = models.ManyToManyField(Ip, blank=True, related_name="hits", verbose_name="بازدید ها")
    likes_count = models.ManyToManyField(user, blank=True, related_name="likes", 
    verbose_name="تعداد پسند ها")
    download_count = models.ManyToManyField(user, blank=True, related_name="downloads", verbose_name="تعداد دانلود ها")
    comments = GenericRelation(Comment)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="وضعیت انتشار")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = PostManager()

    class Meta:
        verbose_name = "پست"
        verbose_name_plural = "پست ها"
        ordering = ["-created"]

    def __str__(self):
        return self.title

    def thumbnail_img(self):
        return format_html(f"""
            <img width=100 height=75 style='border-radius: 2px;border: 1px solid gray;'
            src='{self.img.url}'>
        """)
    thumbnail_img.short_description = "عکس شما"
