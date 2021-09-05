import os
import shutil

from django.test import RequestFactory

options = {
    "MEDIA_ROOT": os.path.join(os.getcwd(), "tests", "media"),
    "DOWNLOAD_ROOT": os.path.join(os.getcwd(), "tests", "download")
}

def remove_media():
    for path in options.values():
        if os.path.exists(path):
            shutil.rmtree(path)

request = RequestFactory()
