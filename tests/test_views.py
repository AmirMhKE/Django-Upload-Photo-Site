import os

from app.models import Post, Category
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from extension.utils import get_files_list, get_test_form_image, get_test_image

from .base import client, media_paths, remove_media

__all__ = ("AppCountViews", "AccountDashboardViewsTestCase")

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

@override_settings(**media_paths)
class AccountDashboardViewsTestCase(TestCase):
    fixtures = ("fixtures/category_data.json",)

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

        self.post1 = Post(title="test1", publisher=self.user1,
        category=Category.objects.get(pk=20),
        img=get_test_image("tests/test_images/1.jpg"))
        self.post1.save()

        self.post2 = Post(title="test2", publisher=self.user2,
        category=Category.objects.get(pk=19),
        img=get_test_image("tests/test_images/2.jpg"))
        self.post2.save()

        self.post3 = Post(title="test3", publisher=self.super_user1,
        category=Category.objects.get(pk=18),
        img=get_test_image("tests/test_images/3.jpg"))
        self.post3.save()

        self.post4 = Post(title="test4", publisher=self.super_user2,
        category=Category.objects.get(pk=17),
        img=get_test_image("tests/test_images/4.jpg"))
        self.post4.save()

    def test_user_settings_view_permission(self):
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

    def test_user_delete_view(self):
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

    def test_post_create_view(self):
        initial_data = {}

        client.login(username="test1", password="12345")

        initial_data["title"] = "test4"
        initial_data["img"] = get_test_form_image("tests/test_images/profile.jpg")
        initial_data["category"] = "1"
        client.post("/account/dashboard/create/", initial_data)
        self.assertTrue(Post.objects.filter(title="test4").exists())

        initial_data["title"] = "test5"
        initial_data["img"] = get_test_form_image("tests/test_images/5.jpg")
        initial_data["category"] = "3"
        client.post("/account/test2/dashboard/create/", initial_data)
        self.assertFalse(Post.objects.filter(title="test5").exists())

        client.post("/account/test3/dashboard/create/", initial_data)
        self.assertFalse(Post.objects.filter(title="test5").exists())

        client.login(username="test3", password="12345")

        initial_data["img"] = get_test_form_image("tests/test_images/5.jpg")
        client.post("/account/dashboard/create/", initial_data)
        self.assertTrue(Post.objects.filter(title="test5").exists())

        initial_data["title"] = "test6"
        initial_data["img"] = get_test_form_image("tests/test_images/6.jpg")
        initial_data["category"] = "5"
        client.post("/account/test2/dashboard/create/", initial_data)
        self.assertTrue(Post.objects.filter(title="test6").exists())

        initial_data["title"] = "test7"
        initial_data["img"] = get_test_form_image("tests/test_images/7.jpg")
        initial_data["category"] = "7"
        client.post("/account/test4/dashboard/create/", initial_data)
        self.assertFalse(Post.objects.filter(title="test7").exists())

    def test_post_edit_view(self):
        initial_data = {}

        client.login(username="test1", password="12345")

        initial_data["title"] = "Test1"
        initial_data["img"] = ""
        initial_data["category"] = str(self.post1.category.pk)
        req_url = reverse("account:post_edit", kwargs={"slug": self.post1.slug})
        client.post(req_url, initial_data)
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.title, "Test1")

        initial_data["title"] = "Test2"
        initial_data["img"] = ""
        initial_data["category"] = str(self.post2.category.pk)
        req_url = reverse("account:post_edit", kwargs={"slug": self.post2.slug, 
        "username": "test2"})
        client.post(req_url, initial_data)
        self.post2.refresh_from_db()
        self.assertNotEqual(self.post2.title, "Test2")

        initial_data["title"] = "Test3"
        initial_data["img"] = ""
        initial_data["category"] = str(self.post3.category.pk)
        req_url = reverse("account:post_edit", kwargs={"slug": self.post3.slug, 
        "username": "test3"})
        client.post(req_url, initial_data)
        self.post3.refresh_from_db()
        self.assertNotEqual(self.post3.title, "Test3")

        client.login(username="test3", password="12345")

        initial_data["title"] = "Test3"
        initial_data["img"] = ""
        initial_data["category"] = str(self.post3.category.pk)
        req_url = reverse("account:post_edit", kwargs={"slug": self.post3.slug})
        client.post(req_url, initial_data)
        self.post3.refresh_from_db()
        self.assertEqual(self.post3.title, "Test3")

        initial_data["title"] = "Test2"
        initial_data["img"] = ""
        initial_data["category"] = str(self.post2.category.pk)
        req_url = reverse("account:post_edit", kwargs={"slug": self.post2.slug, 
        "username": "test2"})
        client.post(req_url, initial_data)
        self.post2.refresh_from_db()
        self.assertEqual(self.post2.title, "Test2")

        initial_data["title"] = "Test4"
        initial_data["img"] = ""
        initial_data["category"] = str(self.post4.category.pk)
        req_url = reverse("account:post_edit", kwargs={"slug": self.post4.slug, 
        "username": "test4"})
        client.post(req_url, initial_data)
        self.post4.refresh_from_db()
        self.assertNotEqual(self.post4.title, "Test4")

    def test_post_edit_view_get_object(self):
        not_found_status, success_status = 404, 200

        client.login(username="test3", password="12345")

        req_url = reverse("account:post_edit", kwargs={"slug": self.post3.slug,
        "username": "test3"})
        req = client.get(req_url)
        self.assertEqual(req.status_code, success_status)

        req_url = reverse("account:post_edit", kwargs={"slug": self.post2.slug,
        "username": "test2"})
        req = client.get(req_url)
        self.assertEqual(req.status_code, success_status)

        req_url = reverse("account:post_edit", kwargs={"slug": self.post1.slug,
        "username": "test1"})
        req = client.get(req_url)
        self.assertEqual(req.status_code, success_status)

        req_url = reverse("account:post_edit", kwargs={"slug": self.post3.slug,
        "username": "test1"})
        req = client.get(req_url)
        self.assertEqual(req.status_code, not_found_status)

        req_url = reverse("account:post_edit", kwargs={"slug": self.post3.slug,
        "username": "test2"})
        req = client.get(req_url)
        self.assertEqual(req.status_code, not_found_status)

        req_url = reverse("account:post_edit", kwargs={"slug": self.post2.slug,
        "username": "test3"})
        req = client.get(req_url)
        self.assertEqual(req.status_code, not_found_status)

        req_url = reverse("account:post_edit", kwargs={"slug": self.post1.slug,
        "username": "test3"})
        req = client.get(req_url)
        self.assertEqual(req.status_code, not_found_status)

        req_url = reverse("account:post_edit", kwargs={"slug": self.post1.slug,
        "username": "test2"})
        req = client.get(req_url)
        self.assertEqual(req.status_code, not_found_status)

        req_url = reverse("account:post_edit", kwargs={"slug": self.post2.slug,
        "username": "test1"})
        req = client.get(req_url)
        self.assertEqual(req.status_code, not_found_status)

    def test_post_delete_view(self):
        client.login(username="test1", password="12345")

        req_url = reverse("account:post_delete", kwargs={"slug": self.post1.slug})
        client.post(req_url)
        self.assertFalse(Post.objects.filter(title="test1").exists())

        req_url = reverse("account:post_delete", kwargs={"slug": self.post2.slug,
        "username": "test2"})
        client.post(req_url)
        self.assertTrue(Post.objects.filter(title="test2").exists())

        req_url = reverse("account:post_delete", kwargs={"slug": self.post3.slug,
        "username": "test3"})
        client.post(req_url)
        self.assertTrue(Post.objects.filter(title="test3").exists())

        client.login(username="test3", password="12345")

        req_url = reverse("account:post_delete", kwargs={"slug": self.post3.slug})
        client.post(req_url)
        self.assertFalse(Post.objects.filter(title="test3").exists())

        req_url = reverse("account:post_delete", kwargs={"slug": self.post2.slug,
        "username": "test2"})
        client.post(req_url)
        self.assertFalse(Post.objects.filter(title="test2").exists())

        req_url = reverse("account:post_delete", kwargs={"slug": self.post4.slug,
        "username": "test4"})
        client.post(req_url)
        self.assertTrue(Post.objects.filter(title="test4").exists())

    @staticmethod
    def tearDown():
        remove_media()
