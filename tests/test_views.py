import json
import os

from app.models import Post
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from extension.utils import get_files_list, get_test_image

from .base import client, media_paths, remove_media

__all__ = ("AppCountViews",)

User = get_user_model()

@override_settings(**media_paths)
class AppCountViews(TestCase):
    def setUp(self):
        self.post = Post(title="test1", 
        img=get_test_image("tests/test_images/1.jpg"))
        self.post.save()

        User.objects.create_user(username="test1", 
        email="test1@gmail.com", password="12345")

    def test_like_view(self):
        req_url = reverse("like", kwargs={"slug": self.post.slug})
        client.login(username="test1", password="12345")

        req = client.get(req_url)
        res = json.loads(req.content)
        self.assertDictEqual(res, {"action": "like", "count": 1})

        req = client.get(req_url)
        res = json.loads(req.content)
        self.assertDictEqual(res, {"action": "dislike", "count": 0})

        req = client.get(req_url)
        res = json.loads(req.content)
        self.assertDictEqual(res, {"action": "like", "count": 1})

        req = client.get(req_url)
        res = json.loads(req.content)
        self.assertDictEqual(res, {"action": "dislike", "count": 0})

    def test_download_view(self):
        req_url = reverse("download", kwargs={"slug": self.post.slug})
        client.login(username="test1", password="12345")

        req = client.get(req_url)
        self.assertEqual(req.status_code, 200)

        img_path = get_files_list(os.path.join(settings.DOWNLOAD_ROOT, self.post.slug))[0]
        self.assertEqual(int(req.headers["Content-Length"]), len(open(img_path, "rb").read()))

    @staticmethod
    def tearDown():
        remove_media()
