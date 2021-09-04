import os
import shutil

options = {
    "MEDIA_ROOT": os.path.join(os.getcwd(), "tests", "media"),
    "DOWNLOAD_ROOT": os.path.join(os.getcwd(), "tests", "download")
}

def remove_media():
    for path in options.values():
        shutil.rmtree(path)
