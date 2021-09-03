import os
import shutil

from django.test import TestCase, override_settings
from extensions.utils import get_files_list, get_test_image
from app.models import Category, Post
from PIL import Image
from .base import options


class CategoryModelTestCase(TestCase):
    def setUp(self):
        Category.objects.create(title="عکس کلاسیک", slug="classic", position=1, status=False)
        Category.objects.create(title="عکس طبیعت", slug="nature", position=0, status=True)
        Category.objects.create(title="عکس ماشین", slug="car", position=2, status=True)

    def test_active_manager(self):
        all_cat = Category.objects.all()
        active_cat = Category.objects.active()

        self.assertEqual(all_cat.count(), 3)
        self.assertEqual(active_cat.count(), 2)

    def test_ordering(self):
        first_cat = Category.objects.first()
        last_cat = Category.objects.last()

        self.assertEqual(first_cat.status, True)
        self.assertEqual(first_cat.position, 0)
        self.assertEqual(last_cat.status, False)
        self.assertEqual(last_cat.position, 1)

@override_settings(**options)
class PostModelTestCase(TestCase):
    def setUp(self):
        Post(title="test1", img=get_test_image("tests/test_images/1.jpg")).save()
        Post(title="test2", img=get_test_image("tests/test_images/2.jpg")).save()
        Post(title="test3", img=get_test_image("tests/test_images/3.jpg")).save()
        Post(title="test4", img=get_test_image("tests/test_images/4.jpg")).save()
        Post(title="test5", img=get_test_image("tests/test_images/5.jpg")).save()

    def test_unique_slug(self):
        objects = Post.objects.all()

        self.assertNotEqual(objects[0].slug, objects[1].slug)
        self.assertNotEqual(objects[3].slug, objects[1].slug)
        self.assertNotEqual(objects[2].slug, objects[4].slug)
        self.assertNotEqual(objects[2].slug, objects[1].slug)
        self.assertNotEqual(objects[4].slug, objects[3].slug)
        self.assertNotEqual(objects[3].slug, objects[0].slug)
        self.assertNotEqual(objects[1].slug, objects[4].slug)

    def test_image_size(self):
        dwr = options["DOWNLOAD_ROOT"]
        obj1 = Post.objects.first()
        obj2 = Post.objects.get(pk=2)
        obj3 = Post.objects.get(pk=3)

        self.assertEqual(int(obj1.original_size_image.split("×")[0]),
        Image.open(get_files_list(os.path.join(dwr, obj1.slug))[-1]).width)
        self.assertEqual(int(obj1.original_size_image.split("×")[1]),
        Image.open(get_files_list(os.path.join(dwr, obj1.slug))[-1]).height)

        self.assertEqual(int(obj2.original_size_image.split("×")[0]),
        Image.open(get_files_list(os.path.join(dwr, obj2.slug))[-1]).width)
        self.assertEqual(int(obj2.original_size_image.split("×")[1]),
        Image.open(get_files_list(os.path.join(dwr, obj2.slug))[-1]).height)

        self.assertEqual(int(obj3.original_size_image.split("×")[0]),
        Image.open(get_files_list(os.path.join(dwr, obj3.slug))[-1]).width)
        self.assertEqual(int(obj3.original_size_image.split("×")[1]),
        Image.open(get_files_list(os.path.join(dwr, obj3.slug))[-1]).height)

    def tearDown(self):
        shutil.rmtree(options["MEDIA_ROOT"])
        shutil.rmtree(options["DOWNLOAD_ROOT"])
