import os
import shutil

from django.db.models.signals import post_init, post_save, pre_delete
from django.dispatch import receiver

from .models import CustomUser


@receiver(post_init, sender=CustomUser)
def auto_backup_old_profile_image(sender, instance, **kwargs):
    try:
        instance.old_profile_image = instance.profile_image
    except ValueError:
        if hasattr(instance, "old_profile_image"):
            delattr(instance, "old_profile_image")

@receiver(post_save, sender=CustomUser)
def delete_old_profile_image(sender, instance, **kwargs):
    try:
        if hasattr(instance, "old_profile_image"):
            if instance.old_profile_image != instance.profile_image:
                os.remove(instance.old_profile_image.path)
    except ValueError:
        pass

# ? When account deleted, profile user remove
@receiver(pre_delete, sender=CustomUser)
def delete_user_profile_folder(sender, instance, **kwargs):
    try:
        user_profile_dir_name = os.path.dirname(instance.profile_image.path)
        shutil.rmtree(user_profile_dir_name)
    except ValueError:
        pass
    