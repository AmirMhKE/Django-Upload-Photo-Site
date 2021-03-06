from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from .base import client, auth

__all__ = ("MixinsTestCase",)

User = get_user_model()

@override_settings(**auth)
class MixinsTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username="test1",
        email="test1@gmail.com", password="12345")
        User.objects.create_user(username="test2",
        email="test2@gmail.com", password="12345")
        User.objects.create_user(username="test3",
        email="test3@gmail.com", password="12345", is_superuser=True)
        User.objects.create_user(username="test4",
        email="test4@gmail.com", password="12345", is_superuser=True)
        User.objects.create_user(username="test5",
        email="test5@gmail.com", password="12345", is_admin=True)
        User.objects.create_user(username="test6",
        email="test6@gmail.com", password="12345", is_admin=True)

    def test_login_required_mixin(self):
        redirect_status, success_status = 302, 200

        req = client.get("/account/dashboard/")
        self.assertEqual(req.status_code, redirect_status)

        client.login(username="test1", password="12345")

        req = client.get("/account/dashboard/")
        self.assertEqual(req.status_code, success_status)

        client.login(username="test2", password="12345")

        req = client.get("/account/dashboard/")
        self.assertEqual(req.status_code, success_status)

        client.login(username="test3", password="12345")

        req = client.get("/account/statistics/")
        self.assertEqual(req.status_code, success_status)

        client.login(username="test4", password="12345")

        req = client.get("/account/statistics/")
        self.assertEqual(req.status_code, success_status)

    def test_superuser_or_user_mixin(self):
        redirect_status, success_status = 302, 200

        client.login(username="test1", password="12345")

        req = client.get("/account/dashboard/")
        self.assertEqual(req.status_code, success_status)

        req = client.get("/account/test2/dashboard/")
        self.assertEqual(req.status_code, redirect_status)

        req = client.get("/account/test3/dashboard/")
        self.assertEqual(req.status_code, redirect_status)

        req = client.get("/account/test5/dashboard/")
        self.assertEqual(req.status_code, redirect_status)

        client.login(username="test3", password="12345")

        req = client.get("/account/statistics/")
        self.assertEqual(req.status_code, success_status)

        req = client.get("/account/test1/dashboard/")
        self.assertEqual(req.status_code, success_status)

        req = client.get("/account/test4/dashboard/")
        self.assertEqual(req.status_code, redirect_status)

        req = client.get("/account/test5/dashboard/")
        self.assertEqual(req.status_code, redirect_status)

        client.login(username="test5", password="12345")

        req = client.get("/account/statistics/")
        self.assertEqual(req.status_code, success_status)

        req = client.get("/account/test1/dashboard/")
        self.assertEqual(req.status_code, success_status)

        req = client.get("/account/test4/dashboard/")
        self.assertEqual(req.status_code, success_status)

        req = client.get("/account/test6/dashboard/")
        self.assertEqual(req.status_code, redirect_status)
