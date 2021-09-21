import os
import json

from app.models import Post
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from extension.utils import get_files_list, get_test_image

from .base import client, media_paths, remove_media

__all__ = ("AppCountViews", "AccountMainViewsTestCase")

User = get_user_model()

@override_settings(**media_paths)
class AppCountViews(TestCase):
    def setUp(self):
        self.post1 = Post(title="test1", 
        img=get_test_image("tests/test_images/1.jpg"))
        self.post1.save()

        self.post2 = Post(title="test2", 
        img=get_test_image("tests/test_images/2.jpg"))
        self.post2.save()

        self.post3 = Post(title="test3", 
        img=get_test_image("tests/test_images/3.jpg"))
        self.post3.save()

        user1 = User.objects.create_user(username="test1", 
        email="test1@gmail.com", password="12345")
        user1.is_superuser = True
        user1.save()

        user2 = User.objects.create_user(username="test2", 
        email="test2@gmail.com", password="12345")
        user2.is_superuser = True
        user2.save()

        user3 = User.objects.create_user(username="test3", 
        email="test3@gmail.com", password="12345")
        user3.is_superuser = True
        user3.save()

    def test_like_view(self):
        req_url = reverse("like", kwargs={"slug": self.post1.slug})
        client.login(username="test1", password="12345")

        req = client.get(req_url)
        self.assertJSONEqual(str(req.content, encoding="utf-8"), {"action": "like", "count": 1})

        req = client.get(req_url)
        self.assertJSONEqual(str(req.content, encoding="utf-8"), {"action": "dislike", "count": 0})

        req = client.get(req_url)
        self.assertJSONEqual(str(req.content, encoding="utf-8"), {"action": "like", "count": 1})

        client.login(username="test2", password="12345")

        req = client.get(req_url)
        self.assertJSONEqual(str(req.content, encoding="utf-8"), {"action": "like", "count": 2})

        req = client.get(req_url)
        self.assertJSONEqual(str(req.content, encoding="utf-8"), {"action": "dislike", "count": 1})

        req = client.get(req_url)
        self.assertJSONEqual(str(req.content, encoding="utf-8"), {"action": "like", "count": 2})

        client.login(username="test3", password="12345")

        req = client.get(req_url)
        self.assertJSONEqual(str(req.content, encoding="utf-8"), {"action": "like", "count": 3})

        req = client.get(req_url)
        self.assertJSONEqual(str(req.content, encoding="utf-8"), {"action": "dislike", "count": 2})

        req = client.get(req_url)
        self.assertJSONEqual(str(req.content, encoding="utf-8"), {"action": "like", "count": 3})

    def test_download_view(self):
        client.login(username="test1", password="12345")

        req_url = reverse("download", kwargs={"slug": self.post1.slug})
        req = client.get(req_url)
        self.assertEqual(req.status_code, 200)

        img_path = get_files_list(os.path.join(settings.DOWNLOAD_ROOT, self.post1.slug))[-1]
        self.assertEqual(int(req.headers["Content-Length"]), len(open(img_path, "rb").read()))

        req_url = reverse("download", kwargs={"slug": self.post2.slug})
        req = client.get(req_url)
        self.assertEqual(req.status_code, 200)

        img_path = get_files_list(os.path.join(settings.DOWNLOAD_ROOT, self.post2.slug))[-1]
        self.assertEqual(int(req.headers["Content-Length"]), len(open(img_path, "rb").read()))

        req_url = reverse("download", kwargs={"slug": self.post3.slug})
        req = client.get(req_url)
        self.assertEqual(req.status_code, 200)

        img_path = get_files_list(os.path.join(settings.DOWNLOAD_ROOT, self.post3.slug))[-1]
        self.assertEqual(int(req.headers["Content-Length"]), len(open(img_path, "rb").read()))

    @staticmethod
    def tearDown():
        remove_media()

class AccountMainViewsTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="test1",
        email="test1@gmail.com", password="12345")
        self.user2 = User.objects.create_user(username="test2",
        email="test2@gmail.com", password="12345")

        self.super_user1 = User.objects.create_user(username="test3",
        email="test3@gmail.com", password="12345")
        self.super_user1.is_superuser = True
        self.super_user1.save()

        self.super_user2 = User.objects.create_user(username="test4",
        email="test4@gmail.com", password="12345")
        self.super_user2.is_superuser = True
        self.super_user2.save()

    def test_user_settings_permission(self):
        initial_data = {
            "first_name": "",
            "last_name": "",
            "username": "",
            "about_me": "",
            "profile_image": "",
            "is_active": "on",
        }

        client.login(username="test1", password="12345")

        initial_data["username"] = "Test1"
        client.post("/account/settings/", initial_data)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, "Test1")

        initial_data["username"] = "Test2"
        client.post("/account/settings/test2", initial_data)
        self.user2.refresh_from_db()        
        self.assertNotEqual(self.user2.username, "Test2")

        initial_data["is_superuser"] = "on"
        initial_data["username"] = "Test3"
        client.post("/account/settings/test3", initial_data)
        self.super_user1.refresh_from_db()
        self.assertNotEqual(self.super_user1.username, "Test3")

        client.login(username="test3", password="12345")

        client.post("/account/settings/", initial_data)
        self.super_user1.refresh_from_db()
        self.assertEqual(self.super_user1.username, "Test3")

        initial_data["is_superuser"] = ""
        initial_data["username"] = "Test2"
        client.post("/account/settings/test2", initial_data)
        self.user2.refresh_from_db()
        self.assertEqual(self.user2.username, "Test2")

        initial_data["is_superuser"] = "on"
        initial_data["username"] = "Test4"
        client.post("/account/settings/test4", initial_data)
        self.super_user2.refresh_from_db()
        self.assertNotEqual(self.super_user2.username, "Test4")

    def test_user_delete(self):
        client.login(username="test1", password="12345")

        client.post("/account/delete/")
        self.assertFalse(User.objects.filter(username="test1").exists())

        client.login(username="test2", password="12345")

        client.post("/account/delete/")
        self.assertFalse(User.objects.filter(username="test2").exists())

        client.login(username="test3", password="12345")

        client.post("/account/delete/")
        self.assertFalse(User.objects.filter(username="test3").exists())

        client.login(username="test4", password="12345")

        client.post("/account/delete/")
        self.assertFalse(User.objects.filter(username="test4").exists())
