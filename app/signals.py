import os
import shutil

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from .models import Post


# ? delete folder image when post object deleted
@receiver(pre_delete, sender=Post)
def image_delete(sender, instance, **kwargs):
    dir_name = os.path.dirname(instance.img.path)
    shutil.rmtree(dir_name)