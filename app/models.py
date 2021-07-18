import os
import shutil
from random import randint

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.html import format_html
from django_jalali.db import models as jmodels
from PIL import Image

user = get_user_model()

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
    last_excessive_request_time = models.DateTimeField(verbose_name="آخرین وقت درخواست غیر مجاز")
    excessive_requests_count = models.PositiveIntegerField(verbose_name="تعداد درخواست های بیش از حد اندازه", null=True, blank=True, default=0)

    class Meta:
        verbose_name = "آیپی"
        verbose_name_plural = "آیپی ها"

    def __str__(self):
        return self.ip_address

def upload_location(instance, filename):
        extension = filename.split(".")[1]

        if extension != "jpg":
            raise ValidationError(f"شما می توانید فقط فایل هایی با پسوند jpg آپلود کنید.")

        return f"images/{instance.slug}/{instance.slug}.{extension}"

class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان عکس")
    slug = models.CharField(max_length=250, unique=True, verbose_name="آدرس عکس", blank=True)
    img = models.ImageField(upload_to=upload_location, verbose_name="عکس شما")
    original_size_image = models.CharField(max_length=50, verbose_name="سایز پیش فرض عکس", null=True, blank=True)
    publisher = models.ForeignKey(user, on_delete=models.CASCADE, null=True, verbose_name="منتشر کننده", related_name="posts")
    category = models.ForeignKey(Category, verbose_name="دسته بندی", related_name="posts", on_delete=models.CASCADE, null=True)
    hits = models.ManyToManyField(Ip, blank=True, related_name="hits", verbose_name="بازدید ها")
    likes_count = models.ManyToManyField(user, blank=True, related_name="likes", 
    verbose_name="تعداد پسند ها")
    download_count = models.ManyToManyField(user, blank=True, related_name="downloads", verbose_name="تعداد دانلود ها")
    created = jmodels.jDateTimeField(auto_now_add=True)
    updated = jmodels.jDateTimeField(auto_now=True)

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

    def save(self, *args, **kwargs):
        # ? if model not created, override save method
        if not self.pk:
            self.slug_save()
            super().save(*args, **kwargs)

            self.img_save()
            super().save(*args, **kwargs)

    def slug_save(self):
        MIN_LENGTH = 25
        MAX_LENGTH = 35

        alph_l = "".join([chr(l).upper() if not c else chr(l).lower() for l in range(65, 91) for c in range(2)])

        if not self.slug:
            random_slug = get_random_string(randint(MIN_LENGTH, MAX_LENGTH), alph_l)
            query = Post.objects.filter(slug=random_slug).exists()

            # ? if random slug wasn't unique
            while query:
                random_slug = get_random_string(randint(MIN_LENGTH, MAX_LENGTH), alph_l)
                query = Post.objects.filter(slug=random_slug).exists()

            self.slug = random_slug

    def img_save(self):
        # ? This image for download
        dir_name = os.path.dirname(self.img.path)
        file_name = os.path.join(dir_name, f"{self.slug}-akscade.jpg")
        dowload_image = Image.open(self.img)
        dowload_image.save(file_name)

        # ? Save size image
        height, width = dowload_image.size
        self.original_size_image = f"{str(width)} × {str(height)}"

        # ? This image for show in site
        with Image.open(self.img) as img:
            img.thumbnail((750, 750))
            img.save(self.img.path)
            img.close()