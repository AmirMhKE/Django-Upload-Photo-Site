import os
from typing import Union

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from extension.utils import compare_similarities_two_images
from PIL import Image, UnidentifiedImageError

User = get_user_model()

def get_dashboard_publisher(request: HttpRequest, username: Union[str, None] = None) -> User:
    """
    This function get user of the dashboard.
    """
    if username is None:
        user = User.objects.prefetch_related("posts").get(pk=request.user.pk)
    else:
        user = get_object_or_404(User.objects.prefetch_related("posts"), 
        username__iexact=username)

    return user

def get_dashboard_success_url(request: HttpRequest, dashboard_user: User) -> str:
    """
    This function get success url when a 
    post created or updated in the dashboard.
    """
    user = get_dashboard_publisher(request, dashboard_user.username)

    if request.user == user:
        success_url = reverse("account:dashboard")
    else:
        success_url = reverse("account:dashboard", 
        kwargs={"username": user.username})

    return success_url

def check_similar_images(model, data, instance_pk=None):
    """
    This function checks if there is a image 
    similar to the one you image submitted.
    return True if image not exists else return False.
    model Post getted from out file because
    code 'from app.model import Post' has error occurred. 
    """
    try:
        query = model.objects.values_list("img")

        if instance_pk is not None:
            query = query.exclude(pk=instance_pk)

        check_images = (
            compare_similarities_two_images(Image.open(data), 
            Image.open(os.path.join(settings.MEDIA_ROOT, img_path[0])))
            for img_path in query.iterator()
        )

        if any(check_images):
            return False
    except UnidentifiedImageError:
        pass
    
    return True

def check_number_uploaded_images(model, user):
    """
    This function limits the user to uploading too many images 
    and the user can not upload a large number of images per day.
    model Post getted from out file because
    code 'from app.model import Post' has error occurred.
    """
    max_count = settings.MAX_IMAGE_UPLOAD_COUNT
    
    if not user.is_superuser:
        now_time = timezone.now().date()
        query = model.objects.select_related("publisher") \
        .filter(publisher=user, created__date=now_time)

        if query.count() >= max_count:
            return False, max_count

    return True, max_count     
