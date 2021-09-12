import os
import shutil

from django.test import Client, RequestFactory

media_paths = {
    "MEDIA_ROOT": os.path.join(os.getcwd(), "tests", "media"),
    "DOWNLOAD_ROOT": os.path.join(os.getcwd(), "tests", "download"),
}

options = {
    "MIN_BLOCK_TIME_EXCESSIVE_REQUESTS": 1,
    "MAX_BLOCK_TIME_EXCESSIVE_REQUESTS": 1,
    "MAX_IMAGE_UPLOAD_COUNT": 2
}

def remove_media():
    for path in media_paths.values():
        if os.path.exists(path):
            shutil.rmtree(path)

client = Client()
request = RequestFactory()
