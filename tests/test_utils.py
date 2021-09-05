from django.http import QueryDict
from django.test import SimpleTestCase
from extensions.utils import (compare_similarities_two_images, get_client_ip,
                              param_request_get_to_url_param)
from PIL import Image

from .base import request

__all__ = ("ExtensionUtilsTestCase",)

class ExtensionUtilsTestCase(SimpleTestCase):
    def test_get_client_ip(self):
        req = request.get("/")

        # ? In Local Host
        self.assertEqual(get_client_ip(req), "127.0.0.1")

    def test_compare_similarities_two_images(self):
        base_dir = "tests/test_images/"

        self.assertEqual(compare_similarities_two_images(
        Image.open(base_dir + "1.jpg"), Image.open(base_dir + "1.jpg")), True)
        self.assertEqual(compare_similarities_two_images(
        Image.open(base_dir + "2.jpg"), Image.open(base_dir + "2.jpg")), True)
        self.assertEqual(compare_similarities_two_images(
        Image.open(base_dir + "3.jpg"), Image.open(base_dir + "3.jpg")), True)
        self.assertEqual(compare_similarities_two_images(
        Image.open(base_dir + "4.jpg"), Image.open(base_dir + "4.jpg")), True)
        self.assertEqual(compare_similarities_two_images(
        Image.open(base_dir + "5.jpg"), Image.open(base_dir + "5.jpg")), True)

        self.assertEqual(compare_similarities_two_images(
       Image.open(base_dir + "1.jpg"),Image.open(base_dir + "2.jpg")), False)
        self.assertEqual(compare_similarities_two_images(
       Image.open(base_dir + "3.jpg"),Image.open(base_dir + "5.jpg")), False)
        self.assertEqual(compare_similarities_two_images(
       Image.open(base_dir + "2.jpg"),Image.open(base_dir + "4.jpg")), False)
        self.assertEqual(compare_similarities_two_images(
       Image.open(base_dir + "6.jpg"),Image.open(base_dir + "5.jpg")), False)
        self.assertEqual(compare_similarities_two_images(
       Image.open(base_dir + "2.jpg"),Image.open(base_dir + "3.jpg")), False)

    def test_param_request_get_to_url_param(self):
        test_param_1 = "publisher=test1&ordering=-likes&search=post1"
        test_param_2 = "publisher=test2&ordering=created&search=post2"
        test_param_3 = "publisher=test3&ordering=-hits&search=post3"
        test_param_4 = "publisher=test4&ordering=download&search=post4"
        test_param_5 = "publisher=test5&ordering=likes&search=post5"

        self.assertEqual(param_request_get_to_url_param(QueryDict(test_param_1)), 
        "?" + test_param_1)
        self.assertEqual(param_request_get_to_url_param(QueryDict(test_param_2)), 
        "?" + test_param_2)
        self.assertEqual(param_request_get_to_url_param(QueryDict(test_param_3)), 
        "?" + test_param_3)
        self.assertEqual(param_request_get_to_url_param(QueryDict(test_param_4)), 
        "?" + test_param_4)
        self.assertEqual(param_request_get_to_url_param(QueryDict(test_param_5)), 
        "?" + test_param_5)
