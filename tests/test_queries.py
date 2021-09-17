from app.models import Category, Post, UserHit
from app.templatetags.sidebar_tags import (get_most_viewed_category_from_user,
                                           suggestion_posts)
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, override_settings
from extensions.utils import get_test_image

from .base import media_paths, remove_media, request

__all__ = ("QueriesTestCase",)

User = get_user_model()

@override_settings(**media_paths)
class QueriesTestCase(TestCase):
    fixtures = ("fixtures/category_data.json",)

    def setUp(self):
        self.user1 = User.objects.create_user(username="test1", 
        email="test1@gmail.com", password="12345")
        self.user2 = User.objects.create_user(username="test2", 
        email="test2@gmail.com", password="12345")
        self.user3 = User.objects.create_user(username="test3", 
        email="test3@gmail.com", password="12345")

        post1 = Post(title="test1", category=Category.objects.get(pk=1),
        img=get_test_image("tests/test_images/1.jpg"))
        post1.save()
        post2 = Post(title="test2", category=Category.objects.get(pk=1),
        img=get_test_image("tests/test_images/2.jpg"))
        post2.save()
        post3 = Post(title="test3", category=Category.objects.get(pk=2),
        img=get_test_image("tests/test_images/3.jpg"))
        post3.save()
        post4 = Post(title="test4", category=Category.objects.get(pk=2),
        img=get_test_image("tests/test_images/4.jpg"))
        post4.save()
        post5 = Post(title="test5", category=Category.objects.get(pk=3),
        img=get_test_image("tests/test_images/5.jpg"))
        post5.save()
        post6 = Post(title="test6", category=Category.objects.get(pk=3),
        img=get_test_image("tests/test_images/6.jpg"))
        post6.save()

        UserHit(post=post1, user=self.user1).save()
        UserHit(post=post2, user=self.user1).save()
        UserHit(post=post5, user=self.user1).save()
        UserHit(post=post3, user=self.user2).save()
        UserHit(post=post4, user=self.user2).save()
        UserHit(post=post6, user=self.user2).save()
        UserHit(post=post5, user=self.user3).save()
        UserHit(post=post6, user=self.user3).save()
        UserHit(post=post2, user=self.user3).save()

    def test_get_most_viewed_category_from_user(self):
        query = get_most_viewed_category_from_user(self.user1)
        self.assertEqual(query.first().category.pk, 1)

        query = get_most_viewed_category_from_user(self.user2)
        self.assertEqual(query.first().category.pk, 2)

        query = get_most_viewed_category_from_user(self.user3)
        self.assertEqual(query.first().category.pk, 3)

    def test_get_suggestion_posts(self):
        sid, num = "sidebar_items", 5
        req = request.get("/")

        req.user = AnonymousUser()
        query = suggestion_posts(req, num)
        self.assertEqual(len(query[sid]), num)

        req.user = self.user1
        query = suggestion_posts(req, num)
        self.assertEqual(query[sid][0].category.id, 1)
        self.assertEqual(query[sid][1].category.pk, 1)
        self.assertNotEqual(query[sid][2].category.pk, 1)
        self.assertNotEqual(query[sid][3].category.pk, 1)
        self.assertNotEqual(query[sid][4].category.pk, 1)

        req.user = self.user2
        query = suggestion_posts(req, num)
        self.assertEqual(query[sid][0].category.id, 2)
        self.assertEqual(query[sid][1].category.pk, 2)
        self.assertNotEqual(query[sid][2].category.pk, 2)
        self.assertNotEqual(query[sid][3].category.pk, 2)
        self.assertNotEqual(query[sid][4].category.pk, 2)

        req.user = self.user3
        query = suggestion_posts(req, num)
        self.assertEqual(query[sid][0].category.id, 3)
        self.assertEqual(query[sid][1].category.pk, 3)
        self.assertNotEqual(query[sid][2].category.pk, 3)
        self.assertNotEqual(query[sid][3].category.pk, 3)
        self.assertNotEqual(query[sid][4].category.pk, 3)

    @staticmethod
    def tearDown():
        remove_media()
