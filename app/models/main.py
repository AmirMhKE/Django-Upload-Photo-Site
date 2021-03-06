import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from extension.timestamp import TimeStamp
from extension.utils import (convert_binary_nparray_to_nums,
                             get_file_thumbnail, get_random_str)
from PIL import Image

__all__ = ("Category", "Post")

User = get_user_model()

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
        ordering = ("-status", "position")

    def __str__(self):
        return self.title

def upload_location(instance, filename):
    return f"images/{instance.slug}/{get_random_str(10, 50)}.jpg"

class Post(TimeStamp):
    title = models.CharField(max_length=100, verbose_name="عنوان عکس", db_index=True)
    slug = models.CharField(max_length=250, unique=True, verbose_name="آدرس عکس", blank=True)
    img = models.ImageField(upload_to=upload_location, verbose_name="عکس شما")
    img_hash = models.CharField(max_length=72, verbose_name="اثر انگشت عکس", 
    null=True, blank=True)
    original_size_image = models.CharField(max_length=50, verbose_name="سایز پیش فرض عکس", 
    null=True, blank=True)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, null=True, 
    verbose_name="منتشر کننده", related_name="posts")
    category = models.ForeignKey(Category, verbose_name="دسته بندی", related_name="posts", 
    on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "پست"
        verbose_name_plural = "پست ها"
        ordering = ("-created",)

    def __str__(self):
        return self.title

    @classmethod
    def get_fields_name(cls):
        return [field.name for field in cls._meta.get_fields()]

    @classmethod
    def get_related_fields_name(cls):
        return list(filter(lambda x: x != "",
            [field.name if isinstance(field, models.ManyToOneRel) else "" 
            for field in cls._meta.get_fields()]
       ))

    def save(self, *args, **kwargs):
        # ? if model not created
        if not self.pk:
            self.slug_save()
            super().save(*args, **kwargs)

            # ? if model created
            self.img_save()

        # ? if model updated
        super().save(*args, **kwargs)

    def slug_save(self):
        if not self.slug:
            random_slug = get_random_str(25, 35)
            query = Post.objects.filter(slug=random_slug).exists()

            # ? if random slug wasn't unique
            while query:
                random_slug = get_random_str(25, 35)
                query = Post.objects.filter(slug=random_slug).exists()

            self.slug = random_slug

    def img_save(self):
        # ? This image for download
        if not os.path.exists(settings.DOWNLOAD_ROOT):
            os.makedirs(settings.DOWNLOAD_ROOT)

        if not os.path.exists(os.path.join(settings.DOWNLOAD_ROOT, self.slug)):
            os.makedirs(os.path.join(settings.DOWNLOAD_ROOT, self.slug))

        download_image = Image.open(self.img)
        download_image.save(os.path.join(settings.DOWNLOAD_ROOT, self.slug,
        f"{get_random_str(10, 50)}-akscade.jpg"), format=download_image.format)

        # ? Save hash image
        thumbnail = get_file_thumbnail(download_image)
        self.img_hash = convert_binary_nparray_to_nums(thumbnail)

        # ? Save size image
        width, height = download_image.width, download_image.height
        self.original_size_image = f"{str(height)} × {str(width)}"

        # ? This image for show in site
        show_width = settings.SHOW_IMAGE_WIDTH
        show_height = settings.SHOW_IMAGE_HEIGHT
        
        with Image.open(self.img) as img:
            img.thumbnail((show_height, show_width))
            img.save(self.img.path, format=download_image.format)
            img.close()
