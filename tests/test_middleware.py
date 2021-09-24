import time

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from .base import client, options, auth

__all__ = ("RequestProcessMiddlewareTestCase",)

User = get_user_model()

@override_settings(**options, **auth)
class RequestProcessMiddlewareTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username="test1", 
        email="test1@gmail.com", password="12345")

        super_user = User.objects.create_user(username="test2", 
        email="test2@gmail.com", password="12345")
        super_user.is_superuser = True
        super_user.save()

    def test_check_user_request_count(self):
        client.login(username="test1", password="12345")
        client.get("/")
        client.get("/")
        client.get("/")

        user = User.objects.get(username="test1")

        self.assertEqual(user.all_requests_count, 3)

        client.login(username="test2", password="12345")
        client.get("/")
        client.get("/")
        client.get("/")

        user = User.objects.get(username="test2")

        self.assertEqual(user.all_requests_count, 3)

    def test_check_excessive_requests(self):
        # ? ===== Anonymouse User Test =====
        for _ in range(10):
            client.get("/")

        self.assertEqual(client.get("/").status_code, 404)
        time.sleep(1)
        self.assertEqual(client.get("/").status_code, 200)

        # ? ===== Normal User Test =====
        client.login(username="test1", password="12345")

        for _ in range(10):
            client.get("/")

        user = User.objects.get(username="test1")

        self.assertEqual(client.get("/").status_code, 404)
        time.sleep(1)
        self.assertEqual(client.get("/").status_code, 200)
        self.assertEqual(user.excessive_requests_count, 1)

        # ? ===== Super User Test =====
        client.login(username="test2", password="12345")

        for _ in range(10):
            client.get("/")

        user = User.objects.get(username="test2")

        self.assertEqual(client.get("/").status_code, 200)
        time.sleep(1)
        self.assertEqual(client.get("/").status_code, 200)
        self.assertEqual(user.excessive_requests_count, 0)
