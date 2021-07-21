import os
import shutil

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.conf import settings

from .models import Post


# ? delete folder image when post object deleted
@receiver(pre_delete, sender=Post)
def image_delete(sender, instance, **kwargs):
    dir_name = os.path.dirname(instance.img.path)
    download_dir_name = settings.DOWNLOAD_ROOT / instance.slug
    shutil.rmtree(dir_name)
    shutil.rmtree(download_dir_name)