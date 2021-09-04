from os import path

from django.test import TestCase, override_settings
from extensions.utils import get_files_list, get_test_image
from app.models import Category, Post
from PIL import Image
from .base import options, remove_media


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
    mdr = options["MEDIA_ROOT"]
    dwr = options["DOWNLOAD_ROOT"]

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
        objects = Post.objects.all()
        obj1, obj2, obj3 = objects[4], objects[3], objects[2]

        self.assertEqual(int(obj1.original_size_image.split("×")[1]),
        Image.open(get_files_list(path.join(self.dwr, obj1.slug))[-1]).width)
        self.assertEqual(int(obj1.original_size_image.split("×")[0]),
        Image.open(get_files_list(path.join(self.dwr, obj1.slug))[-1]).height)

        self.assertEqual(int(obj2.original_size_image.split("×")[1]),
        Image.open(get_files_list(path.join(self.dwr, obj2.slug))[-1]).width)
        self.assertEqual(int(obj2.original_size_image.split("×")[0]),
        Image.open(get_files_list(path.join(self.dwr, obj2.slug))[-1]).height)

        self.assertEqual(int(obj3.original_size_image.split("×")[1]),
        Image.open(get_files_list(path.join(self.dwr, obj3.slug))[-1]).width)
        self.assertEqual(int(obj3.original_size_image.split("×")[0]),
        Image.open(get_files_list(path.join(self.dwr, obj3.slug))[-1]).height)

    def test_exists_media_folders(self):
        objects = Post.objects.all()
        obj1, obj2, obj3 = objects[0], objects[1], objects[2]

        self.assertEqual(path.exists(path.join(self.mdr, "images", obj1.slug)), True)
        self.assertEqual(path.exists(path.join(self.dwr, obj1.slug)), True)

        self.assertEqual(path.exists(path.join(self.mdr, "images", obj2.slug)), True)
        self.assertEqual(path.exists(path.join(self.dwr, obj2.slug)), True)

        self.assertEqual(path.exists(path.join(self.mdr, "images", obj3.slug)), True)
        self.assertEqual(path.exists(path.join(self.dwr, obj3.slug)), True)

    def test_signal_delete_media_folders_images(self):
        objects = Post.objects.all()
        obj1, obj2, obj3 = objects[4], objects[3], objects[2]

        obj1_slug, obj2_slug, obj3_slug = obj1.slug, obj2.slug, obj3.slug
        obj1.delete()
        obj2.delete()
        obj3.delete()

        self.assertEqual(path.exists(path.join(self.mdr, "images", obj1_slug)), False)
        self.assertEqual(path.exists(path.join(self.dwr, obj1_slug)), False)

        self.assertEqual(path.exists(path.join(self.mdr, "images", obj2_slug)), False)
        self.assertEqual(path.exists(path.join(self.dwr, obj2_slug)), False)

        self.assertEqual(path.exists(path.join(self.mdr, "images", obj3_slug)), False)
        self.assertEqual(path.exists(path.join(self.dwr, obj3_slug)), False)

    def test_signal_delete_old_images(self):
        objects = Post.objects.all()
        obj1, obj2, obj3 = objects[0], objects[1], objects[2]

        old_media_img_path_1 = path.join(self.mdr, "images", obj1.slug)
        old_download_img_path_1 = path.join(self.dwr, obj1.slug)

        obj1.img = get_test_image("tests/test_images/1.jpg")
        obj1.save()

        old_media_img_path_2 = path.join(self.mdr, "images", obj2.slug)
        old_download_img_path_2 = path.join(self.dwr, obj2.slug)
        
        obj2.img = get_test_image("tests/test_images/2.jpg")
        obj2.save()

        old_media_img_path_3 = path.join(self.mdr, "images", obj3.slug)
        old_download_img_path_3 = path.join(self.dwr, obj3.slug)
        
        obj3.img = get_test_image("tests/test_images/4.jpg")
        obj3.save()

        self.assertEqual(len(get_files_list(old_media_img_path_1)), 1)
        self.assertEqual(len(get_files_list(old_download_img_path_1)), 1)

        self.assertEqual(len(get_files_list(old_media_img_path_2)), 1)
        self.assertEqual(len(get_files_list(old_download_img_path_2)), 1)

        self.assertEqual(len(get_files_list(old_media_img_path_3)), 1)
        self.assertEqual(len(get_files_list(old_download_img_path_3)), 1)    

    @staticmethod
    def tearDown():
        remove_media()
