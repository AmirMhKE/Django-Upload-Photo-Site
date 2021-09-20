from os import path

from account.models import CustomUser as User
from app.models import Category, Post
from django.test import TestCase, override_settings
from extension.utils import get_files_list, get_test_image
from PIL import Image

from .base import media_paths, remove_media

__all__ = (
    "CategoryModelTestCase", "PostModelTestCase",
    "UserModelTestCase"
)

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

        self.assertTrue(first_cat.status)
        self.assertEqual(first_cat.position, 0)
        self.assertFalse(last_cat.status)
        self.assertEqual(last_cat.position, 1)

@override_settings(**media_paths)
class PostModelTestCase(TestCase):
    mdr = media_paths["MEDIA_ROOT"]
    dwr = media_paths["DOWNLOAD_ROOT"]

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

        self.assertTrue(path.exists(path.join(self.mdr, "images", obj1.slug)))
        self.assertTrue(path.exists(path.join(self.dwr, obj1.slug)))

        self.assertTrue(path.exists(path.join(self.mdr, "images", obj2.slug)))
        self.assertTrue(path.exists(path.join(self.dwr, obj2.slug)))

        self.assertTrue(path.exists(path.join(self.mdr, "images", obj3.slug)))
        self.assertTrue(path.exists(path.join(self.dwr, obj3.slug)))

    def test_signal_delete_media_folders_images(self):
        objects = Post.objects.all()
        obj1, obj2, obj3 = objects[4], objects[3], objects[2]

        obj1_slug, obj2_slug, obj3_slug = obj1.slug, obj2.slug, obj3.slug
        obj1.delete()
        obj2.delete()
        obj3.delete()

        self.assertFalse(path.exists(path.join(self.mdr, "images", obj1_slug)))
        self.assertFalse(path.exists(path.join(self.dwr, obj1_slug)))

        self.assertFalse(path.exists(path.join(self.mdr, "images", obj2_slug)))
        self.assertFalse(path.exists(path.join(self.dwr, obj2_slug)))

        self.assertFalse(path.exists(path.join(self.mdr, "images", obj3_slug)))
        self.assertFalse(path.exists(path.join(self.dwr, obj3_slug)))

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

@override_settings(**media_paths)
class UserModelTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username="test1", email="test1@gmail.com",
        password="12345")
        user2 = User.objects.create_user(username="test2", email="test2@gmail.com",
        password="12345")
        user3 = User.objects.create_user(username="test3", email="test3@gmail.com",
        password="12345")

        user1.profile_image = get_test_image("tests/test_images/profile.jpg")
        user2.profile_image = get_test_image("tests/test_images/profile.jpg")
        user3.profile_image = get_test_image("tests/test_images/profile.jpg")

        user1.save()
        user2.save()
        user3.save()

    def test_signal_auto_backup_old_profile_image(self):
        users = User.objects.all()
        user1, user2, user3 = users[0], users[1], users[2]

        self.assertEqual(user1.old_profile_image.path, user1.profile_image.path)
        self.assertEqual(user2.old_profile_image.path, user2.profile_image.path)
        self.assertEqual(user3.old_profile_image.path, user3.profile_image.path)

    def test_signal_delete_old_profile_image(self):
        users = User.objects.all()
        user1, user2, user3 = users[0], users[1], users[2]

        old_user1_profile_path = user1.profile_image.path
        old_user2_profile_path = user1.profile_image.path
        old_user3_profile_path = user1.profile_image.path

        user1.profile_image = get_test_image("tests/test_images/profile2.jpg")
        user2.profile_image = get_test_image("tests/test_images/profile2.jpg")
        user3.profile_image = get_test_image("tests/test_images/profile2.jpg")

        user1.save()
        user2.save()
        user3.save()

        self.assertFalse(path.exists(old_user1_profile_path))
        self.assertFalse(path.exists(old_user2_profile_path))
        self.assertFalse(path.exists(old_user3_profile_path))

    def test_signal_delete_user_profile_folder(self):
        users = User.objects.all()
        user1, user2, user3 = users[0], users[1], users[2]

        user1_profile_dir = path.dirname(user1.profile_image.path)
        user2_profile_dir = path.dirname(user2.profile_image.path)
        user3_profile_dir = path.dirname(user3.profile_image.path)

        user1.delete()
        user2.delete()
        user3.delete()

        self.assertFalse(path.exists(user1_profile_dir))
        self.assertFalse(path.exists(user2_profile_dir))
        self.assertFalse(path.exists(user3_profile_dir))

    def test_signal_auto_is_admin_field_trigger(self):
        users = User.objects.all()
        user1, user2, user3 = users[0], users[1], users[2]

        user1.is_admin = True
        user2.is_admin = True
        user3.is_admin = True

        user1.save()
        user2.save()
        user3.save()

        self.assertTrue(user1.is_superuser)
        self.assertTrue(user1.is_admin)

        self.assertTrue(user2.is_superuser)
        self.assertTrue(user2.is_admin)

        self.assertTrue(user3.is_superuser)
        self.assertTrue(user3.is_admin)

    def test_get_name_or_username(self):
        users = User.objects.all()
        user1, user2, user3 = users[0], users[1], users[2]

        self.assertEqual(user1.get_name_or_username, user1.username)
        self.assertEqual(user2.get_name_or_username, user2.username)
        self.assertEqual(user3.get_name_or_username, user3.username)

        user1.first_name = "امیر"
        user2.first_name = "آرمان"
        user3.first_name = "اصغر"

        user1.last_name = "محمدی"
        user2.last_name = "ایمانی"
        user3.last_name = "خدایار نژاد"

        user1.save()
        user2.save()
        user3.save()

        self.assertEqual(user1.get_name_or_username, 
        (user1.first_name + " " + user1.last_name))
        self.assertEqual(user2.get_name_or_username, 
        (user2.first_name + " " + user2.last_name))
        self.assertEqual(user3.get_name_or_username, 
        (user3.first_name + " " + user3.last_name))

    @staticmethod
    def tearDown():
        remove_media()
