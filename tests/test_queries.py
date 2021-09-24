from account.models import AnonymousUser
from account.statistics import user_posts_statistics
from app.models import Category, Download, Hit, Ip, Like, Post, UserHit
from app.templatetags.sidebar_tags import (get_most_viewed_category_from_user,
                                           suggestion_posts)
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from extension.utils import get_test_image
from jdatetime import datetime

from .base import media_paths, remove_media, request

__all__ = ("QueriesTestCase",)

User = get_user_model()

@override_settings(**media_paths)
class QueriesTestCase(TestCase):
    fixtures = ("fixtures/category_data.json",)

    def setUp(self):
        ip1 = Ip(ip_address="192.168.43.102")
        ip1.save()
        ip2 = Ip(ip_address="192.168.43.103")
        ip2.save()
        ip3 = Ip(ip_address="192.168.43.104")
        ip3.save()

        self.user1 = User.objects.create_user(username="test1", 
        email="test1@gmail.com", password="12345")
        self.user2 = User.objects.create_user(username="test2", 
        email="test2@gmail.com", password="12345")
        self.user3 = User.objects.create_user(username="test3", 
        email="test3@gmail.com", password="12345")

        post1 = Post(title="test1", category=Category.objects.get(pk=1),
        img=get_test_image("tests/test_images/1.jpg"), publisher=self.user1)
        post1.save()
        post2 = Post(title="test2", category=Category.objects.get(pk=1),
        img=get_test_image("tests/test_images/2.jpg"), publisher=self.user1)
        post2.save()
        post3 = Post(title="test3", category=Category.objects.get(pk=2),
        img=get_test_image("tests/test_images/3.jpg"), publisher=self.user2)
        post3.save()
        post4 = Post(title="test4", category=Category.objects.get(pk=2),
        img=get_test_image("tests/test_images/4.jpg"), publisher=self.user2)
        post4.save()
        post5 = Post(title="test5", category=Category.objects.get(pk=3),
        img=get_test_image("tests/test_images/5.jpg"), publisher=self.user3)
        post5.save()
        post6 = Post(title="test6", category=Category.objects.get(pk=3),
        img=get_test_image("tests/test_images/6.jpg"), publisher=self.user3)
        post6.save()

        self.create_new_related_model("userhit", post1, self.user1)
        self.create_new_related_model("userhit", post2, self.user1)
        self.create_new_related_model("userhit", post5, self.user1)
        self.create_new_related_model("userhit", post3, self.user2)
        self.create_new_related_model("userhit", post4, self.user2)
        self.create_new_related_model("userhit", post6, self.user2)
        self.create_new_related_model("userhit", post5, self.user3)
        self.create_new_related_model("userhit", post6, self.user3)
        self.create_new_related_model("userhit", post2, self.user3)

        self.create_new_related_model("hit", post1, ip1, datetime(1400, 5, 23))
        self.create_new_related_model("hit", post2, ip2, datetime(1400, 5, 19))
        self.create_new_related_model("hit", post1, ip2, datetime(1400, 5, 14))
        self.create_new_related_model("like", post1, self.user1, datetime(1400, 6, 1))
        self.create_new_related_model("like", post2, self.user1, datetime(1400, 5, 21))
        self.create_new_related_model("like", post2, self.user2, datetime(1400, 5, 29))
        self.create_new_related_model("download", post1, self.user3, datetime(1400, 5, 24))
        self.create_new_related_model("download", post2, self.user3, datetime(1400, 6, 4))
        self.create_new_related_model("download", post1, self.user2, datetime(1400, 6, 11))

        self.create_new_related_model("hit", post3, ip3, datetime(1400, 5, 5))
        self.create_new_related_model("hit", post4, ip3, datetime(1400, 5, 5))
        self.create_new_related_model("hit", post3, ip1, datetime(1400, 5, 5))
        self.create_new_related_model("like", post3, self.user2, datetime(1400, 5, 6))
        self.create_new_related_model("like", post4, self.user1, datetime(1400, 5, 6))
        self.create_new_related_model("like", post4, self.user2, datetime(1400, 5, 6))
        self.create_new_related_model("download", post3, self.user3, datetime(1400, 5, 7))
        self.create_new_related_model("download", post3, self.user1, datetime(1400, 5, 7))
        self.create_new_related_model("download", post4, self.user1, datetime(1400, 5, 7))

        self.create_new_related_model("hit", post6, ip2, datetime(1400, 5, 10))
        self.create_new_related_model("hit", post5, ip1, datetime(1400, 5, 10))
        self.create_new_related_model("hit", post6, ip1, datetime(1400, 5, 11))
        self.create_new_related_model("like", post5, self.user3, datetime(1400, 5, 12))
        self.create_new_related_model("like", post6, self.user3, datetime(1400, 5, 12))
        self.create_new_related_model("like", post5, self.user2, datetime(1400, 5, 12))
        self.create_new_related_model("download", post5, self.user1, datetime(1400, 5, 13))
        self.create_new_related_model("download", post6, self.user1, datetime(1400, 5, 14))
        self.create_new_related_model("download", post6, self.user2, datetime(1400, 5, 14))

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
        self.assertEqual(query[sid][0].category.pk, 1)
        self.assertEqual(query[sid][1].category.pk, 1)
        self.assertNotEqual(query[sid][2].category.pk, 1)
        self.assertNotEqual(query[sid][3].category.pk, 1)
        self.assertNotEqual(query[sid][4].category.pk, 1)

        req.user = self.user2
        query = suggestion_posts(req, num)
        self.assertEqual(query[sid][0].category.pk, 2)
        self.assertEqual(query[sid][1].category.pk, 2)
        self.assertNotEqual(query[sid][2].category.pk, 2)
        self.assertNotEqual(query[sid][3].category.pk, 2)
        self.assertNotEqual(query[sid][4].category.pk, 2)

        req.user = self.user3
        query = suggestion_posts(req, num)
        self.assertEqual(query[sid][0].category.pk, 3)
        self.assertEqual(query[sid][1].category.pk, 3)
        self.assertNotEqual(query[sid][2].category.pk, 3)
        self.assertNotEqual(query[sid][3].category.pk, 3)
        self.assertNotEqual(query[sid][4].category.pk, 3)

    def test_user_posts_statistics(self):
        days_ago = 99999

        query = user_posts_statistics(self.user1, days_ago)
        dates_list = ["1400/06/11", "1400/06/04", "1400/06/01", "1400/05/29",
        "1400/05/24", "1400/05/23", "1400/05/21", "1400/05/19", "1400/05/14"]
        hits_list = [0, 0, 0, 0, 0, 1, 0, 1, 1]
        likes_list = [0, 0, 1, 1, 0, 0, 1, 0, 0]
        downloads_list = [1, 1, 0, 0, 1, 0, 0, 0, 0]
        self.assertListEqual(query["dates"], dates_list)
        self.assertListEqual(query["hits"], hits_list)
        self.assertListEqual(query["likes"], likes_list)
        self.assertListEqual(query["downloads"], downloads_list)

        query = user_posts_statistics(self.user2, days_ago, True)
        dates_list = ["1400/05/05", "1400/05/06", "1400/05/07"]
        hits_list = [3, 0, 0]
        likes_list = [0, 3, 0]
        downloads_list = [0, 0, 3]
        self.assertListEqual(query["dates"], dates_list)
        self.assertListEqual(query["hits"], hits_list)
        self.assertListEqual(query["likes"], likes_list)
        self.assertListEqual(query["downloads"], downloads_list)

        query = user_posts_statistics(self.user3, days_ago)
        dates_list = ["1400/05/14", "1400/05/13", "1400/05/12", 
        "1400/05/11", "1400/05/10"]
        hits_list = [0, 0, 0, 1, 2]
        likes_list = [0, 0, 3, 0, 0]
        downloads_list = [2, 1, 0, 0, 0]
        self.assertListEqual(query["dates"], dates_list)
        self.assertListEqual(query["hits"], hits_list)
        self.assertListEqual(query["likes"], likes_list)
        self.assertListEqual(query["downloads"], downloads_list)

    @staticmethod
    def create_new_related_model(model_name, post, ip_or_user, created_or_updated=None):
        models = {
            "hit": Hit,
            "userhit": UserHit,
            "like": Like,
            "download": Download
        }

        if created_or_updated is None:
            created_or_updated = datetime.now()

        if model_name == "hit":
            model = models[model_name](post=post, ip_address=ip_or_user)
        elif model_name == "like":
            models[model_name]._meta.get_field("updated").auto_now = False
            model = models[model_name](post=post, user=ip_or_user, 
            updated=created_or_updated, status=True)
        else:
            model = models[model_name](post=post, user=ip_or_user)

        model.save()

        model.created = created_or_updated
        model.save()

    @staticmethod
    def tearDown():
        remove_media()
