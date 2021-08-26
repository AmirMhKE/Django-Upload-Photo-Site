import os

from account.mixins import LoginRequiredMixin
from app.models import Download, Like, Post
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.encoding import smart_str
from django.views import View
from extensions.utils import get_files_list, get_random_str
from PIL import Image

__all__ = ("DownloadView", "LikeView")

class DownloadView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Post, slug=kwargs.get("slug"))
        file_name = get_files_list(os.path.join(settings.DOWNLOAD_ROOT, obj.slug))[-1]
        img = Image.open(file_name)
         
        extension = obj.img.path.split(".")[-1]
        content = \
        f"attachment; filename={os.path.basename(f'{get_random_str(10, 50)}-akscade.{extension}')}" 
        response = HttpResponse(img, content_type="application/force-download")
        response["Content-Disposition"] = content
        response["X-Sendfile"] = smart_str(img)

        download_query = Download.objects.filter(post=obj, user=request.user)
        if not download_query.exists():
            Download.objects.create(post=obj, user=request.user)

        return response

class LikeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Post, slug=kwargs.get("slug"))
        like_query = Like.objects.filter(post=obj, user=request.user)

        actions = {True: "like", False: "dislike"}
        
        if not like_query.exists():
            Like.objects.create(post=obj, user=request.user, status=True)
            result = {"action": "like", "count": obj.likes.active().count()}
        else:
            like_obj = Like.objects.get(post=obj, user=request.user)
            like_obj.status = not like_obj.status
            like_obj.save()
            result = {"action": actions[like_obj.status], "count": obj.likes.active().count()}

        return JsonResponse(result)
