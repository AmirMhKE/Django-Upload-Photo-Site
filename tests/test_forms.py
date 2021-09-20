from app.models import Post, Category
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from account.forms import UserUpdateForm, PostForm
from extension.utils import get_test_image, get_test_form_image
from .base import options, request, remove_media

__all__ = ("UserUpdateFormTestCase", "PostFormTestCase")

User = get_user_model()

@override_settings(**options)
class UserUpdateFormTestCase(TestCase):
    def setUp(self):
        normal_user = User.objects.create_user(username="test1", 
        email="test1@gamil.com", password="12345")

        super_user = User.objects.create_user(username="test2",
        email="test2@gamil.com", password="12345")
        super_user.is_superuser = True
        super_user.save()

        admin_user = User.objects.create_user(username="test3",
        email="test3@gamil.com", password="12345")
        admin_user.is_admin = True
        admin_user.save()

        self.normal_user = normal_user
        self.super_user= super_user
        self.admin_user = admin_user
        self.initial_data = {
            "first_name": "",
            "last_name": "",
            "username": "",
            "about_me": "",
            "profile_image": "",
            "is_active": "on",
        }

    def test_clean_profile_image(self):
        form_data = self.initial_data.copy()

        # ? ===== Test Normal User =====
        form_data["username"] = self.normal_user.username
        form_data["profile_image"] = get_test_form_image("tests/test_images/profile.jpg")
        form = self.set_form(form_data, self.normal_user)
        self.assertTrue(form.is_valid())

        form_data["profile_image"] = get_test_form_image("tests/test_images/bad_image.jpg")
        form = self.set_form(form_data, self.normal_user)
        self.assertEqual(form.errors.as_data()["profile_image"][0].code, "size_invalid")

        form_data["profile_image"] = get_test_form_image("tests/test_images/bad_image2.gif")
        form = self.set_form(form_data, self.normal_user)
        self.assertEqual(form.errors.as_data()["profile_image"][0].code, "format_invalid")

        # ? ===== Test Super User =====
        form_data["is_superuser"] = "on"
        form_data["username"] = self.super_user.username
        form_data["profile_image"] = get_test_form_image("tests/test_images/profile.jpg")
        form = self.set_form(form_data, self.super_user)
        self.assertTrue(form.is_valid())

        form_data["profile_image"] = get_test_form_image("tests/test_images/bad_image.jpg")
        form = self.set_form(form_data, self.super_user)
        self.assertEqual(form.errors.as_data()["profile_image"][0].code, "size_invalid")

        form_data["profile_image"] = get_test_form_image("tests/test_images/bad_image2.gif")
        form = self.set_form(form_data, self.super_user)
        self.assertEqual(form.errors.as_data()["profile_image"][0].code, "format_invalid")

        # ? ===== Test Admin User =====
        form_data["username"] = self.admin_user.username
        form_data["profile_image"] = get_test_form_image("tests/test_images/profile.jpg")
        form = self.set_form(form_data, self.admin_user)
        self.assertTrue(form.is_valid())

        form_data["profile_image"] = get_test_form_image("tests/test_images/bad_image.jpg")
        form = self.set_form(form_data, self.admin_user)
        self.assertEqual(form.errors.as_data()["profile_image"][0].code, "size_invalid")

        form_data["profile_image"] = get_test_form_image("tests/test_images/bad_image2.gif")
        form = self.set_form(form_data, self.admin_user)
        self.assertEqual(form.errors.as_data()["profile_image"][0].code, "format_invalid")

    def test_clean_username(self):
        form_data = self.initial_data.copy()

        # ? ===== Test Normal User =====
        form_data["username"] = "tEsT1"
        form = self.set_form(form_data, self.normal_user)
        self.assertTrue(form.is_valid())

        form_data["username"] = "Test21"
        form = self.set_form(form_data, self.normal_user)
        self.assertFalse(form.is_valid())

        # ? ===== Test Super User =====
        form_data["is_superuser"] = "on"
        form_data["username"] = "TEst2"
        form = self.set_form(form_data, self.super_user)
        self.assertTrue(form.is_valid())

        form_data["username"] = "Test43"
        form = self.set_form(form_data, self.super_user)
        self.assertFalse(form.is_valid())

        # ? ===== Test Admin User =====
        form_data["username"] = "tEST3"
        form = self.set_form(form_data, self.admin_user)
        self.assertTrue(form.is_valid())

        form_data["username"] = "Test56"
        form = self.set_form(form_data, self.admin_user)
        self.assertFalse(form.is_valid())

    def test_check_full_name(self):
        form_data = self.initial_data.copy()

        # ? ===== Test Normal User =====
        form_data["username"] = self.normal_user.username
        form_data["first_name"] = "علی"
        form_data["last_name"] = "نوری"
        form = self.set_form(form_data, self.normal_user)
        self.assertTrue(form.is_valid())

        form_data["first_name"] = ""
        form = self.set_form(form_data, self.normal_user)
        self.assertEqual(form.errors.as_data()["first_name"][0].code, "full_name_invalid")

        form_data["first_name"] = "علی"
        form_data["last_name"] = ""
        form = self.set_form(form_data, self.normal_user)
        self.assertEqual(form.errors.as_data()["first_name"][0].code, "full_name_invalid")

        # ? ===== Test Super User =====
        form_data["is_superuser"] = "on"
        form_data["username"] = self.super_user.username
        form_data["first_name"] = "اکبر"
        form_data["last_name"] = "کشاورز"
        form = self.set_form(form_data, self.super_user)
        self.assertTrue(form.is_valid())

        form_data["first_name"] = ""
        form = self.set_form(form_data, self.super_user)
        self.assertEqual(form.errors.as_data()["first_name"][0].code, "full_name_invalid")

        form_data["first_name"] = "اکبر"
        form_data["last_name"] = ""
        form = self.set_form(form_data, self.super_user)
        self.assertEqual(form.errors.as_data()["first_name"][0].code, "full_name_invalid")

        # ? ===== Test Admin User =====
        form_data["username"] = self.admin_user.username
        form_data["first_name"] = "مبین"
        form_data["last_name"] = "بیات"
        form = self.set_form(form_data, self.admin_user)
        self.assertTrue(form.is_valid())

        form_data["first_name"] = ""
        form = self.set_form(form_data, self.admin_user)
        self.assertEqual(form.errors.as_data()["first_name"][0].code, "full_name_invalid")

        form_data["first_name"] = "مبین"
        form_data["last_name"] = ""
        form = self.set_form(form_data, self.admin_user)
        self.assertEqual(form.errors.as_data()["first_name"][0].code, "full_name_invalid")

    def test_change_user_self_level(self):
        form_data = self.initial_data.copy()

        # ? ===== Test Normal User =====
        form_data["username"] = self.normal_user.username
        form_data["is_active"] = "on"
        form_data["is_superuser"] = ""
        form = self.set_form(form_data, self.normal_user)
        self.assertTrue(form.is_valid())

        form_data["is_active"] = ""
        form = self.set_form(form_data, self.normal_user)
        self.assertEqual(form.errors.as_data()["is_active"][0].code, "permission_error")

        form_data["is_active"] = "on"
        form_data["is_superuser"] = "on"
        form = self.set_form(form_data, self.normal_user)
        self.assertEqual(form.errors.as_data()["is_superuser"][0].code, "permission_error")
        # ? ===== Test Super User =====
        form_data["username"] = self.super_user.username
        form_data["is_active"] = "on"
        form_data["is_superuser"] = "on"
        form = self.set_form(form_data, self.super_user)
        self.assertTrue(form.is_valid())

        form_data["is_active"] = ""
        form = self.set_form(form_data, self.super_user)
        self.assertEqual(form.errors.as_data()["is_active"][0].code, "permission_error")

        form_data["is_active"] = "on"
        form_data["is_superuser"] = ""
        form = self.set_form(form_data, self.super_user)
        self.assertEqual(form.errors.as_data()["is_superuser"][0].code, "permission_error")
        # ? ===== Test Admin User =====
        form_data["username"] = self.admin_user.username
        form_data["is_active"] = "on"
        form_data["is_superuser"] = "on"
        form = self.set_form(form_data, self.admin_user)
        self.assertTrue(form.is_valid())

        form_data["is_active"] = ""
        form = self.set_form(form_data, self.admin_user)
        self.assertEqual(form.errors.as_data()["is_active"][0].code, "permission_error")

        form_data["is_active"] = "on"
        form_data["is_superuser"] = ""
        form = self.set_form(form_data, self.admin_user)
        self.assertEqual(form.errors.as_data()["is_superuser"][0].code, "permission_error")

    def test_change_other_users_level(self):
        form_data = self.initial_data.copy()

        normal_user2 = User.objects.create_user(username="test5", 
        email="test5@gamil.com", password="12345")

        super_user2 = User.objects.create_user(username="test6", 
        email="test6@gamil.com", password="12345")
        super_user2.is_superuser = True
        super_user2.save()

        admin_user2 = User.objects.create_user(username="test7", 
        email="test7@gamil.com", password="12345")
        admin_user2.is_admin = True
        admin_user2.save()

        # ? ===== Test Normal User =====
        form_data["username"] = normal_user2.username
        form_data["is_superuser"] = "on"
        form = self.set_form(form_data, normal_user2, self.normal_user)
        self.assertEqual(form.errors.as_data()["is_superuser"][0].code, "permission_error")

        form_data["username"] = self.super_user.username
        form_data["is_superuser"] = ""
        form = self.set_form(form_data, self.super_user, self.normal_user)
        self.assertEqual(form.errors.as_data()["is_superuser"][0].code, "permission_error")

        form_data["username"] = self.admin_user.username
        form_data["is_superuser"] = ""
        form = self.set_form(form_data, self.admin_user, self.normal_user)
        self.assertEqual(form.errors.as_data()["is_superuser"][0].code, "permission_error")
        # ? ===== Test Super User =====
        form_data["username"] = self.normal_user.username
        form_data["is_superuser"] = "on"
        form = self.set_form(form_data, self.normal_user, self.super_user)
        self.assertEqual(form.errors.as_data()["is_superuser"][0].code, "permission_error")

        self.normal_user.is_superuser = False
        self.normal_user.save()

        form_data["username"] = super_user2.username
        form_data["is_superuser"] = ""
        form = self.set_form(form_data, super_user2, self.super_user)
        self.assertEqual(form.errors.as_data()["is_superuser"][0].code, "permission_error")

        form_data["username"] = self.admin_user
        form_data["is_superuser"] = ""
        form = self.set_form(form_data, self.admin_user, self.super_user)
        self.assertEqual(form.errors.as_data()["is_superuser"][0].code, "permission_error")
        # ? ===== Test Admin User =====
        form_data["username"] = self.normal_user.username
        form_data["is_superuser"] = "on"
        form = self.set_form(form_data, self.normal_user, self.admin_user)
        self.assertTrue(form.is_valid())

        form_data["username"] = self.super_user.username
        form_data["is_superuser"] = ""
        form = self.set_form(form_data, self.super_user, self.admin_user)
        self.assertTrue(form.is_valid())

        form_data["username"] = admin_user2.username
        form_data["is_superuser"] = ""
        form = self.set_form(form_data, admin_user2, self.admin_user)
        self.assertEqual(form.errors.as_data()["is_superuser"][0].code, "permission_error")

    @staticmethod
    def set_form(form_data, user, req_user=None):
        if req_user is None:
            req_user = user

        req = request.post("account/settings/", form_data)
        req.user = req_user

        kwargs = {
            "data": req.POST,
            "request": req,
            "instance": user
        }

        if form_data["profile_image"]:
            kwargs["files"] = req.FILES

        form = UserUpdateForm(**kwargs)
        return form

    @staticmethod
    def tearDown():
        remove_media()

@override_settings(**options)
class PostFormTestCase(TestCase):
    fixtures = ("fixtures/category_data.json",)

    def setUp(self):
        self.post1 = Post(title="test1", img=get_test_image("tests/test_images/1.jpg"),
        category=Category.objects.get(pk=1))
        self.post1.save()

        self.post2 = Post(title="test2", img=get_test_image("tests/test_images/2.jpg"),
        category=Category.objects.get(pk=4))
        self.post2.save()

        self.post3 = Post(title="test3", img=get_test_image("tests/test_images/3.jpg"),
        category=Category.objects.get(pk=8))
        self.post3.save()

        self.initial_data = {
            "title": "",
            "img": "",
            "category": ""
        }

    def test_create_post(self):
        form_data = self.initial_data.copy()

        form_data["title"] = "post1"
        form_data["img"] = get_test_form_image("tests/test_images/4.jpg")
        form_data["category"] = "12"
        form = self.set_form(form_data)
        self.assertTrue(form.is_valid())

        form_data["title"] = "post2"
        form_data["img"] = get_test_form_image("tests/test_images/5.jpg")
        form_data["category"] = "9"
        form = self.set_form(form_data)
        self.assertTrue(form.is_valid())

        form_data["title"] = "post3"
        form_data["img"] = get_test_form_image("tests/test_images/6.jpg")
        form_data["category"] = "15"
        form = self.set_form(form_data)
        self.assertTrue(form.is_valid())

    def test_update_post(self):
        form_data = self.initial_data.copy()

        form_data["title"] = "test_post1"
        form_data["category"] = str(self.post1.category.pk)
        form = self.set_form(form_data, self.post1)
        self.assertTrue(form.is_valid())

        form_data["title"] = self.post1.title
        form_data["category"] = "20"
        form = self.set_form(form_data, self.post1)
        self.assertTrue(form.is_valid())

        form_data["title"] = self.post1.title
        form_data["category"] = str(self.post1.category.pk)
        form_data["img"] = get_test_form_image("tests/test_images/2.jpg")
        form = self.set_form(form_data, self.post1)
        self.assertTrue(form.is_valid())

        form_data["title"] = "test_post2"
        form_data["category"] = str(self.post2.category.pk)
        form_data["img"] = ""
        form = self.set_form(form_data, self.post2)
        self.assertTrue(form.is_valid())

        form_data["title"] = self.post2.title
        form_data["category"] = "18"
        form = self.set_form(form_data, self.post2)
        self.assertTrue(form.is_valid())

        form_data["title"] = self.post2.title
        form_data["category"] = str(self.post2.category.pk)
        form_data["img"] = get_test_form_image("tests/test_images/1.jpg")
        form = self.set_form(form_data, self.post2)
        self.assertTrue(form.is_valid())

        form_data["title"] = "test_post3"
        form_data["category"] = str(self.post3.category.pk)
        form_data["img"] = ""
        form = self.set_form(form_data, self.post3)
        self.assertTrue(form.is_valid())

        form_data["title"] = self.post3.title
        form_data["category"] = "14"
        form = self.set_form(form_data, self.post3)
        self.assertTrue(form.is_valid())

        form_data["title"] = self.post3.title
        form_data["category"] = str(self.post3.category.pk)
        form_data["img"] = get_test_form_image("tests/test_images/7.jpg")
        form = self.set_form(form_data, self.post3)
        self.assertTrue(form.is_valid())

    def test_clean_img(self):
        form_data = self.initial_data.copy()

        form_data["title"] = self.post1.title
        form_data["category"] = str(self.post1.category.pk)
        form_data["img"] = get_test_image("tests/test_images/bad_image.jpg")
        form = self.set_form(form_data, self.post1)
        self.assertEqual(form.errors.as_data()["img"][0].code, "size_invalid")

        form_data["img"] = get_test_image("tests/test_images/bad_image2.gif")
        form = self.set_form(form_data, self.post1)
        self.assertEqual(form.errors.as_data()["img"][0].code, "format_invalid")

        form_data["title"] = self.post2.title
        form_data["category"] = str(self.post2.category.pk)
        form_data["img"] = get_test_image("tests/test_images/bad_image.jpg")
        form = self.set_form(form_data, self.post2)
        self.assertEqual(form.errors.as_data()["img"][0].code, "size_invalid")
        
        form_data["img"] = get_test_image("tests/test_images/bad_image2.gif")
        form = self.set_form(form_data, self.post2)
        self.assertEqual(form.errors.as_data()["img"][0].code, "format_invalid")

        form_data["title"] = self.post3.title
        form_data["category"] = str(self.post3.category.pk)
        form_data["img"] = get_test_image("tests/test_images/bad_image.jpg")
        form = self.set_form(form_data, self.post3)
        self.assertEqual(form.errors.as_data()["img"][0].code, "size_invalid")
        
        form_data["img"] = get_test_image("tests/test_images/bad_image2.gif")
        form = self.set_form(form_data, self.post3)
        self.assertEqual(form.errors.as_data()["img"][0].code, "format_invalid")

    @staticmethod
    def set_form(form_data, instance=None):
        req = request.post("account/dashboard/create/", form_data)

        kwargs = {
            "data": req.POST,
        }

        if form_data["img"]:
            kwargs["files"] = req.FILES

        if instance is not None:
            kwargs["instance"] = instance

        form = PostForm(**kwargs)
        return form

    @staticmethod
    def tearDown():
        remove_media()
