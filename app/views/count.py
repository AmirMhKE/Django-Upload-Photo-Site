import os

from account.mixins import LoginRequiredMixin
from app.models import Download, Like, Post
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.encoding import smart_str
from django.views import View
from extension.utils import get_files_list, get_random_str

__all__ = ("DownloadView", "LikeView")

class DownloadView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Post, slug=kwargs.get("slug"))
        file_name = get_files_list(os.path.join(settings.DOWNLOAD_ROOT, obj.slug))[-1]

        with open(file_name, "rb") as img:
            content = \
            f"attachment; filename={os.path.basename(f'{get_random_str(10, 50)}-akscade.jpg')}" 

            response = HttpResponse(img.read(), content_type="application/force-download")
            response["Content-Disposition"] = content
            response["X-Sendfile"] = smart_str(img.read())

            img.close()

        Download.objects.get_or_create(post=obj, user=request.user)

        return response

class LikeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        actions = {True: "like", False: "dislike"}
        obj = get_object_or_404(Post, slug=kwargs.get("slug"))
        
        like_obj = Like.objects.get_or_create(post=obj, user=request.user)[0]
        like_obj.status = not like_obj.status
        like_obj.save()
        
        result = {"action": actions[like_obj.status], "count": obj.likes.active().count()}

        return JsonResponse(result)
