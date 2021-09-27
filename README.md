# Django Upload Photo Site
**This is a site for uploading your photos and share with others.**

Photos are downloadable and you can like the photos.
You can also edit or delete your photos.

**Technologies used:**

 - Programming language: [Python](https://www.python.org/)
 - Backend web framework: [Django](https://www.djangoproject.com/)
 - UI framework: [Bootstrap](https://getbootstrap.com/)
 - Database: [Postgresql](https://www.postgresql.org/)
 - Deploy platform: [Fandogh](https://www.fandogh.cloud/) - [More information](https://docs.fandogh.cloud/docs/source-deployments/source-django)

## How to install and run application
```bash
pip install virtualenv
python -m virtualenv .venv
source .venv/bin/activate
git clone https://github.com/AmirMhKEDjango-Upload-Photo-Site
cd Django-Upload-Photo-Site
pip install -r requirements.txt
pip install -r dev-requirements.txt
```
Fill in the .env file settings to run the application.

```python
# https://djecrety.ir/
SECRET_KEY = ''

DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1']

EMAIL = ''

# if DB_ENV is True don't need fill DB_NAME, DB_USER, ... and database_url getted from environ 
DB_ENV = False

DB_NAME = ''
DB_USER = ''
DB_PASSWORD = ''
DB_HOST = ''
DB_PORT = 5432

# https://console.cloud.google.com/
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

```
And you can change custom application settings in config/settings/app_settings.py:
```python
POST_LIST_PAGE_SIZE = 30
DASHBOARD_POST_LIST_PAGE_SIZE = 15

VALID_IMAGE_FORMATS = ["JPEG", "PNG"]
MAX_IMAGE_UPLOAD_COUNT = 5 # In per day

MIN_BLOCK_TIME_EXCESSIVE_REQUESTS = 600 # Seconds
MAX_BLOCK_TIME_EXCESSIVE_REQUESTS = 900 # Seconds
MINIMUM_DIFFERENCE_REQUESTS = 1.0 # second float
MAX_COUNT_EXCESSIVE_REQUESTS = 5

MAIN_CATEGORIES_NUMBER = 5
USER_LAST_POSTS_COUNT = 6
SIDEBAR_ITEMS_COUNT = 6

SHOW_IMAGE_WIDTH = 1000
SHOW_IMAGE_HEIGHT = 1000
MIN_IMAGE_WIDTH = 300
MIN_IMAGE_HEIGHT = 300

RECENT_DAYS_STATISTICS_POSTS_NUMBER = 15
STATISTICS_POSTS_REVERSE = False

SIDEBAR_TAG_TITLES = {
    "suggestion": "عکس های پیشنهادی برای شما",
    "popular": "محبوب ترین عکس ها",
    "download": "پر دانلود ترین عکس ها",
    "hit": "پر بازدید ترین عکس ها",
}
```

Database migration and run project:

```bash
python manage.py migrate
python manage.py loaddata fixtures/category_data.json
python manage.py createuser -l admin
python manage.py runserver
```
   ## Todo features:
   

 - [ ] Like, download and share photos
 - [ ] Create, edit and delete photos
 - [ ] Filter the order of photos based on the newest, most popular, most visited and ...
 - [ ] Search by username or photo title or both
 - [ ] Various statistics from your account
 - [ ] Edit account
 - [ ] Statistics of the number of views, likes and recent downloads of posts uploaded by you
 - [ ] Photo management panel
 - [ ] Preventing uploading photos with inappropriate format or very small size
 - [ ] Preventing uploading duplicate photos on the site
 - [ ] Suggest photos based on user visits
 - [ ] User public profile
 - [ ] Preventing DDOS attacks to some extent
 - [ ] And other features ...
## Test
if you want run the test, run this code and your database user 
must have access to create the database.

    python manage.py test --verbosity 2
    