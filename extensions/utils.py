import os
import string
from pathlib import Path
from random import randint

import imagehash
from django.core.files import File
from django.http import HttpRequest, QueryDict
from django.utils.crypto import get_random_string


def get_random_str(min_length, max_length):
    """
    This simple function return random character with your min length
    and max length with ascii letters
    """
    alph_l = string.ascii_letters
    random_length = randint(min_length, max_length)
    random_string = get_random_string(random_length, alph_l)
    return random_string

def get_files_list(path: str) -> list:
    """
    This function return list files with sorted by last modified
    """
    try:
        result = []
        paths = sorted(Path(path).iterdir(), key=os.path.getctime)

        for image in paths:
            result.append(os.path.join(path, image))
    except FileNotFoundError:
        pass
    
    return result

def get_client_ip(request: HttpRequest) -> str:
    """
    This function get ip from request
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(",")[0]
    else:
        ip_address = request.META.get("REMOTE_ADDR")

    return ip_address

def set_default_data_forms(data: dict, initial_data: dict) -> dict:
    """
    This function return default data forms when forms invalid,
    Because in Django, when even the forms are wrong, 
    they do not display the initial value of the inputs after the return
    """
    for key, _ in data.items():
        try:
            data[key] = initial_data[key]
        except KeyError:
            continue

    return data

def compare_similarities_two_images(image1, image2):
    """
    Short description: The hash (or fingerprint, really) is 
    derived from a 8x8 monochrome thumbnail of the image. 
    But even with such a reduced sample, the similarity comparisons 
    give quite accurate results. Adjust the cutoff to find a balance 
    between false positives and false negatives that is acceptable.
    """    
    image_hash1 = imagehash.average_hash(image1)
    image_hash2 = imagehash.average_hash(image2)
    cutoff = 5

    # ? If the two images are very similar, return True
    if image_hash1 - image_hash2 < cutoff:
        return True
    return False

def param_request_get_to_url_param(request_get: QueryDict) -> str:
    """
    This function convert request.GET QueryDict to url parameters.
    example: <QueryDict: {'search': ['example'], 'publisher': ['username']}>
    converted to --> ?search=example&publisher=username
    """
    result = None

    for index, (key, value) in enumerate(request_get.items()):
        if index == 0:
            result = f"?{key}"
        else:
            result += f"&{key}"

        if value:
            result += f"={value}"

    return result

def get_test_image(path):
    """
    This function returns the image for testing from the desired path.
    """
    return File(open(path, "rb"))
