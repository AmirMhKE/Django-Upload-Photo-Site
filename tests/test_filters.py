from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from app.models import Post, Hit, Like, Download, Ip
from app.filters import PostSearchFilter, PostOrderingFilter
from extensions.utils import get_test_image
from .base import media_paths, remove_media, request

__all__ = ("PostFiltersTestCase",)

User = get_user_model()

@override_settings(**media_paths)
class PostFiltersTestCase(TestCase):
    def setUp(self):
        ip1 = Ip(ip_address="192.168.43.102")
        ip1.save()
        ip2 = Ip(ip_address="192.168.43.103")
        ip2.save()
        ip3 = Ip(ip_address="192.168.43.104")
        ip3.save()

        user1 = User.objects.create_user(username="test1",
        email="test1@gmail.com", password="12345")
        user2 = User.objects.create_user(username="test2",
        email="test2@gmail.com", password="12345")
        user3 = User.objects.create_user(username="test3",
        email="test3@gmail.com", password="12345")

        self.post1 = Post(title="Python Programming", publisher=user1,
        img=get_test_image("tests/test_images/1.jpg"))
        self.post1.save()

        self.post2 = Post(title="Cpp Programming", publisher=user2,
        img=get_test_image("tests/test_images/2.jpg"))
        self.post2.save()

        self.post3 = Post(title="JavaScript Programming", publisher=user3,
        img=get_test_image("tests/test_images/3.jpg"))
        self.post3.save()

        Hit(post=self.post1, ip_address=ip1).save()
        Hit(post=self.post1, ip_address=ip2).save()
        Hit(post=self.post1, ip_address=ip3).save()
        Hit(post=self.post2, ip_address=ip2).save()
        Hit(post=self.post3, ip_address=ip1).save()
        Hit(post=self.post3, ip_address=ip3).save()

        Like(post=self.post2, user=user1).save()
        Like(post=self.post2, user=user2).save()
        Like(post=self.post2, user=user3).save()
        Like(post=self.post3, user=user2).save()
        Like(post=self.post1, user=user1).save()
        Like(post=self.post1, user=user3).save()

        Download(post=self.post3, user=user1).save()
        Download(post=self.post3, user=user2).save()
        Download(post=self.post3, user=user3).save()
        Download(post=self.post1, user=user2).save()
        Download(post=self.post2, user=user1).save()
        Download(post=self.post2, user=user3).save()

    def test_serach_posts_by_title(self):
        posts = Post.objects.all()

        req = request.get("/?title=prog")
        query = PostSearchFilter(req.GET, posts).qs
        self.assertEqual(query.count(), 3)

        req  = request.get("/?title=py")
        query = PostSearchFilter(req.GET, posts).qs
        self.assertEqual(query.count(), 1)
        self.assertEqual(query[0].title, "Python Programming")

        req = request.get("/?title=cp")
        query = PostSearchFilter(req.GET, posts).qs
        self.assertEqual(query.count(), 1)
        self.assertEqual(query[0].title, "Cpp Programming")

        req = request.get("/?title=java")
        query = PostSearchFilter(req.GET, posts).qs
        self.assertEqual(query.count(), 1)
        self.assertEqual(query[0].title, "JavaScript Programming")

        req = request.get("/?title=something")
        query = PostSearchFilter(req.GET, posts).qs
        self.assertEqual(query.count(), 0)

    def test_search_posts_by_publisher(self):
        posts = Post.objects.all()

        req = request.get("/?publisher=1")
        query = PostSearchFilter(req.GET, posts).qs
        self.assertEqual(query.count(), 1)
        self.assertEqual(query[0].publisher.username, "test1")

        req = request.get("/?publisher=2")
        query = PostSearchFilter(req.GET, posts).qs
        self.assertEqual(query.count(), 1)
        self.assertEqual(query[0].publisher.username, "test2")

        req = request.get("/?publisher=3")
        query = PostSearchFilter(req.GET, posts).qs
        self.assertEqual(query.count(), 1)
        self.assertEqual(query[0].publisher.username, "test3")

        req = request.get("/?publisher=somebody")
        query = PostSearchFilter(req.GET, posts).qs
        self.assertEqual(query.count(), 0)

    def test_posts_ordering(self):
        posts = Post.objects.all()

        # ? ===== Created Ordering =====
        req = request.get("/?ordering=-created")
        query = PostOrderingFilter.filter(posts, req.GET.get("ordering"))
        self.assertEqual(query[0].pk, self.post3.pk)
        self.assertEqual(query[1].pk, self.post2.pk)
        self.assertEqual(query[2].pk, self.post1.pk)

        req = request.get("/?ordering=created")
        query = PostOrderingFilter.filter(posts, req.GET.get("ordering"))
        self.assertEqual(query[0].pk, self.post1.pk)
        self.assertEqual(query[1].pk, self.post2.pk)
        self.assertEqual(query[2].pk, self.post3.pk)

        # ? ===== Hits Ordering =====
        req = request.get("/?ordering=-hits")
        query = PostOrderingFilter.filter(posts, req.GET.get("ordering"))
        self.assertEqual(query[0].pk, self.post1.pk)
        self.assertEqual(query[1].pk, self.post3.pk)
        self.assertEqual(query[2].pk, self.post2.pk)

        req = request.get("/?ordering=hits")
        query = PostOrderingFilter.filter(posts, req.GET.get("ordering"))
        self.assertEqual(query[0].pk, self.post2.pk)
        self.assertEqual(query[1].pk, self.post3.pk)
        self.assertEqual(query[2].pk, self.post1.pk)

        # ? ===== Likes Ordering =====
        req = request.get("/?ordering=-likes")
        query = PostOrderingFilter.filter(posts, req.GET.get("ordering"))
        self.assertEqual(query[0].pk, self.post2.pk)
        self.assertEqual(query[1].pk, self.post1.pk)
        self.assertEqual(query[2].pk, self.post3.pk)

        req = request.get("/?ordering=likes")
        query = PostOrderingFilter.filter(posts, req.GET.get("ordering"))
        self.assertEqual(query[0].pk, self.post3.pk)
        self.assertEqual(query[1].pk, self.post1.pk)
        self.assertEqual(query[2].pk, self.post2.pk)

        # ? ===== Downloads Ordering =====
        req = request.get("/?ordering=-downloads")
        query = PostOrderingFilter.filter(posts, req.GET.get("ordering"))
        self.assertEqual(query[0].pk, self.post3.pk)
        self.assertEqual(query[1].pk, self.post2.pk)
        self.assertEqual(query[2].pk, self.post1.pk)

        req = request.get("/?ordering=downloads")
        query = PostOrderingFilter.filter(posts, req.GET.get("ordering"))
        self.assertEqual(query[0].pk, self.post1.pk)
        self.assertEqual(query[1].pk, self.post2.pk)
        self.assertEqual(query[2].pk, self.post3.pk)

    @staticmethod
    def tearDown():
        remove_media()
