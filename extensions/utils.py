import os
import string
from pathlib import Path
from random import randint

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
