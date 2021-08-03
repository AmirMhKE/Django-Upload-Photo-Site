import base64
from io import BytesIO
from random import randint

from django.core.files.base import ContentFile, File
from django.utils.crypto import get_random_string
from PIL import Image


def get_random_str(min_length, max_length):
    alph_l = "".join([chr(l).upper() if not c else chr(l).lower() 
    for l in range(65, 91) for c in range(2)])
    random_length = randint(min_length, max_length)
    random_string = get_random_string(random_length, alph_l)
    return random_string

def convert_base64_image_to_django_form_file(base64_data):
    decoded_image = BytesIO(base64.b64decode(base64_data))
    buffer = BytesIO()
    image_obj = Image.open(decoded_image)
    image_obj.save(fp=buffer, format=image_obj.format)
    byte_file = ContentFile(buffer.getvalue()).file
    random_name = get_random_str(10, 50) + ".jpg"
    form_file = File(byte_file, name=random_name)
    return form_file