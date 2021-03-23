import os
from dotenv import load_dotenv
load_dotenv(verbose=True)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', '194.87.239.17' ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'youtubedev',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
