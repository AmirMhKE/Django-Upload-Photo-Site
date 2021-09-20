import os
import shutil

from django.conf import settings
from django.db.models.signals import post_save, pre_delete
from django.dispatch.dispatcher import receiver
from extension.utils import get_files_list

from .models import Post


# ? delete folder image when post object deleted
@receiver(pre_delete, sender=Post)
def image_delete(sender, instance, **kwargs):
    dir_name = os.path.dirname(instance.img.path)
    download_dir_name = os.path.join(settings.DOWNLOAD_ROOT, instance.slug)
    shutil.rmtree(dir_name)
    shutil.rmtree(download_dir_name)

# ? delete old image if image updated
@receiver(post_save, sender=Post)
def delete_old_images(sender, instance, **kwargs):
    show_path = os.path.join(settings.MEDIA_ROOT, "images", instance.slug)
    show_image_list = get_files_list(show_path)
  
    download_path = os.path.join(settings.DOWNLOAD_ROOT, instance.slug)
    download_image_list = get_files_list(download_path)

    # ? if exists duplicate file
    if len(show_image_list) > 1:
        for img in show_image_list[:-1]:
            os.remove(img)

    if len(download_image_list) > 1:
        for img in download_image_list[:-1]:
            os.remove(img)
