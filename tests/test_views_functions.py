from account.functions import (check_number_uploaded_images,
                               check_similar_images, get_dashboard_publisher,
                               get_dashboard_success_url)
from app.functions import get_post_list_title
from app.models import Post
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from extension.utils import get_test_image

from .base import media_paths, options, remove_media, request

__all__ = ("ViewFunctionsTestCase",)

User = get_user_model()

settings = {**media_paths, **options}

@override_settings(**settings)
class ViewFunctionsTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="test1", 
        email="test1@gmail.com", password="12345")

        self.user2 = User.objects.create_user(username="test2", 
        email="test2@gmail.com", password="12345")

        self.user3 = User.objects.create_user(username="test3", 
        email="test3@gmail.com", password="12345")

        self.superuser = User.objects.create_user(username="test4",
        email="test4@gmail.com", password="12345")
        self.superuser.is_superuser = True
        self.superuser.save()

        self.post1 = Post(title="test1", publisher=self.user1, 
        img=get_test_image("tests/test_images/1.jpg"))
        self.post1.save()

        self.post2 = Post(title="test2", publisher=self.user2, 
        img=get_test_image("tests/test_images/2.jpg"))
        self.post2.save()

        self.post3 = Post(title="test3", publisher=self.user3, 
        img=get_test_image("tests/test_images/3.jpg"))
        self.post3.save()

    def test_get_post_list_title(self):
        default_title = "همه ی عکس ها"

        req = request.get("/")
        title = get_post_list_title(req, default_title)
        self.assertEqual(title, default_title)

        req = request.get("/?search&title=پایتون")
        title = get_post_list_title(req, default_title)
        self.assertEqual(title, f"جستجوی عبارت ' پایتون ' در {default_title}")

        req = request.get("/?search&publisher=amke")
        title = get_post_list_title(req, default_title)
        self.assertEqual(title, f"جستجوی عبارت ' amke ' در {default_title}")

        req = request.get("/?search&title=پایتون&publisher=amke")
        title = get_post_list_title(req, default_title)
        self.assertEqual(title, f"جستجوی عبارت ' پایتون ' در {default_title}")

        req = request.get("/?search&publisher=amke&title=پایتون")
        title = get_post_list_title(req, default_title)
        self.assertEqual(title, f"جستجوی عبارت ' پایتون ' در {default_title}")

    def test_get_dashboard_publisher(self):
        req = request.get("/account/dashboard/")
        req.user = self.user1
        publisher = get_dashboard_publisher(req)
        self.assertEqual(self.user1, publisher)

        req.user = self.user2
        publisher = get_dashboard_publisher(req)
        self.assertEqual(self.user2, publisher)

        req.user = self.user3
        publisher = get_dashboard_publisher(req)
        self.assertEqual(self.user3, publisher)

        req = request.get("/account/test1/dashboard/")
        publisher = get_dashboard_publisher(req, "test1")
        self.assertEqual(self.user1, publisher)

        req = request.get("/account/test2/dashboard/")
        publisher = get_dashboard_publisher(req, "test2")
        self.assertEqual(self.user2, publisher)

        req = request.get("/account/test3/dashboard/")
        req.user = self.user1
        publisher = get_dashboard_publisher(req, "test3")
        self.assertEqual(self.user3, publisher)

    def test_get_dashboard_success_url(self):
        req = request.get("/account/dashboard/")
        req.user = self.user1
        success_url = get_dashboard_success_url(req, self.user1)
        self.assertEqual(success_url, "/account/dashboard/")

        req.user = self.user2
        success_url = get_dashboard_success_url(req, self.user2)
        self.assertEqual(success_url, "/account/dashboard/")

        req.user = self.user3
        success_url = get_dashboard_success_url(req, self.user3)
        self.assertEqual(success_url, "/account/dashboard/")

        success_url = get_dashboard_success_url(req, self.user1)
        self.assertEqual(success_url, "/account/test1/dashboard/")

        success_url = get_dashboard_success_url(req, self.user2)
        self.assertEqual(success_url, "/account/test2/dashboard/")

        req.user = self.user1
        success_url = get_dashboard_success_url(req, self.user3)
        self.assertEqual(success_url, "/account/test3/dashboard/")

    def test_check_similar_images(self):
        check_similar = check_similar_images(Post, 
        get_test_image("tests/test_images/1.jpg"))
        self.assertFalse(check_similar)

        check_similar = check_similar_images(Post, 
        get_test_image("tests/test_images/2.jpg"))
        self.assertFalse(check_similar)

        check_similar = check_similar_images(Post, 
        get_test_image("tests/test_images/3.jpg"))
        self.assertFalse(check_similar)

        check_similar = check_similar_images(Post, 
        get_test_image("tests/test_images/1.jpg"), self.post1.pk)
        self.assertTrue(check_similar)

        check_similar = check_similar_images(Post, 
        get_test_image("tests/test_images/2.jpg"), self.post2.pk)
        self.assertTrue(check_similar)

        check_similar = check_similar_images(Post, 
        get_test_image("tests/test_images/3.jpg"), self.post3.pk)
        self.assertTrue(check_similar)

    def test_check_number_uploaded_images(self):
        check_upload = check_number_uploaded_images(Post, self.user1)
        self.assertTrue(check_upload[0])

        Post(title="user1_test", publisher=self.user1, 
        img=get_test_image("tests/test_images/4.jpg")).save()

        check_upload = check_number_uploaded_images(Post, self.user1)
        self.assertFalse(check_upload[0])

        check_upload = check_number_uploaded_images(Post, self.user2)
        self.assertTrue(check_upload[0])

        Post(title="user2_test", publisher=self.user2, 
        img=get_test_image("tests/test_images/5.jpg")).save()

        check_upload = check_number_uploaded_images(Post, self.user2)
        self.assertFalse(check_upload[0])

        check_upload = check_number_uploaded_images(Post, self.user3)
        self.assertTrue(check_upload[0])

        Post(title="user3_test", publisher=self.user3, 
        img=get_test_image("tests/test_images/6.jpg")).save()

        check_upload = check_number_uploaded_images(Post, self.user3)
        self.assertFalse(check_upload[0])

        self.post1.publisher = self.superuser
        self.post1.save()

        check_upload = check_number_uploaded_images(Post, self.superuser)
        self.assertTrue(check_upload[0])

        self.post2.publisher = self.superuser
        self.post2.save()

        check_upload = check_number_uploaded_images(Post, self.superuser)
        self.assertTrue(check_upload[0])

    @staticmethod
    def tearDown():
        remove_media()
