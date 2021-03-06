"""
Django settings for Knowledge_base project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/level_0_fos/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

from Knowledge_base.search.utils.fos_init import init_fos
from django.core.cache import cache
import json
from django.conf import settings

from Knowledge_base.search.utils.utils import conversion_fos

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x*z_1_+qthz@^a@0v-89o2-6mn(97qdm=s*$60^u4=-(%@j1uz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Knowledge_base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Knowledge_base.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/'),
)

ELASTIC = {
    'ADDRESS': ['114.115.129.20:9200'],
    'INDEX': ['mag_aminer'],
    'DOC_TYPE': '_doc'
}


CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}


REDIS_TIMEOUT = 7*24*60*60
CUBES_REDIS_TIMEOUT = 60*60
NEVER_REDIS_TIMEOUT = 365*24*60*60


LEVEL_0_FOS_URL = 'data/level_0_fos'
FOS_DIR = 'data/fos'

FOS_ANALYSIS_URL = 'data/result.txt'

YEAR_AGG_URL = 'data/year_agg'
PUBLISHER_AGG_URL = 'data/publisher_agg'
FOS_AGG_URL = 'data/fos_agg'
AUTHOR_NAME_AGG_URL = 'data/author_name_agg'


def get_fos_init():

    level_0_fos_url = os.path.join(BASE_DIR, LEVEL_0_FOS_URL)
    fos_dir = os.path.join(BASE_DIR, FOS_DIR)

    # root_fos, fos_dict: format:{ "fos_id":{“name”:name1, "child":[]},....}
    level_0_fos, fos_dict = init_fos(level_0_fos_url, fos_dir)

    level_0_fos_list = []
    level_0_fos_mapper = {} # name -> id
    for fos in level_0_fos:
        level_0_fos_list.append(level_0_fos[fos]['name'])
        level_0_fos_mapper[level_0_fos[fos]['name']] = fos

    return fos_dict, level_0_fos_list, level_0_fos_mapper


def agg_info_init(url):
    agg_info_list = []
    with open(os.path.join(BASE_DIR,url), mode="r") as reader:
        for line in reader:
            elements = json.loads(line)
            agg_info_list.append(elements)
    return agg_info_list


FOS_DICT, LEVEL_0_FOS_LIST, LEVEL_0_FOS_MAPPER = get_fos_init()

PAPER_DETAIL_FIELDS = ['authors', 'title', 'year', 'doi', 'references', 'publisher', 'abstract', "original"]

PAPER_NUM = 264692606
YEAR_AGG_INFO = agg_info_init(YEAR_AGG_URL)
PUBLISHER_AGG_INFO = agg_info_init(PUBLISHER_AGG_URL)
FOS_AGG_INFO = conversion_fos(agg_info_init(FOS_AGG_URL))
AUTHOR_NAME_AGG_INFO = agg_info_init(AUTHOR_NAME_AGG_URL)


def redis_init():
    with open(os.path.join(BASE_DIR, FOS_ANALYSIS_URL), mode="r") as reader:
        for line in reader:
            elements = json.loads(line)
            cache.set(elements['id'], elements['count'], timeout=None)

    for fos in FOS_AGG_INFO:
        cache.set(fos['id'],fos['count'])


redis_init()





