"""
Django settings for locallibrary project.

Generated by 'django-admin startproject' using Django 4.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os

from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

from dotenv import load_dotenv
load_dotenv(BASE_DIR / '.env') # Use only in display

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = "django-insecure-7(_q)0k(nc2yy1l!y+js$fnwry_!zabo92h7r6a5x&=5zi%&$9"
import os
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY', 
    'django-insecure-&psk#na5l=p3q8_a+-$4w1f^lt3lx1c@d*p4x$ymm_rn7pwb87')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

ALLOWED_HOSTS = ['*'] # Quiza sea algo peligroso
# ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(' ')

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    #add our new application
    "catalog.apps.CatalogConfig" #object created in /catalog/apps.py
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "locallibrary.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "locallibrary.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

import dj_database_url

"""db_from_env = dj_database_url.config(
    default='postgres://alumnodb:alumnodb@localhost:5432/psi',
    conn_max_age=500)"""

"""db_from_env = dj_database_url.config(
    default='postgresql://ignacio.nunnez:WQjce6b7izlA@ep-yellow-sun-a20bfr41.eu-central-1.aws.neon.tech/locallibrary?sslmode=require',
    conn_max_age=500)"""
          
"""DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}"""
#The following environment variable, called DATABASE_URL, has to be defined
#at the o.s. level: export DATABASE_URL =
# ’postgres://alumnodb:alumnodb@localhost:5432/psi’
"""DATABASES = {
    'default': dj_database_url.config(
    default='postgresql://alumnodb:alumnodb@localhost:5432/locallibrary',        conn_max_age=600    )}"""

"""DATABASES = {
    'default': dj_database_url.config(
    default='postgresql://ignacio.nunnez:WQjce6b7izlA@ep-yellow-sun-a20bfr41.eu-central-1.aws.neon.tech/locallibrary?sslmode=require',        conn_max_age=600    )}"""
# To use Neon with Django, you have to create a Project on Neon and specify the project connection settings in your settings.py in the same way as for standalone Postgres.

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/London"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "catalog/static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/'

POSTGRESQL_URL = 'postgresql://alumnodb:alumnodb@localhost:5432/locallibrary'
NEON_URL = 'postgresql://ignacio.nunnez:WQjce6b7izlA@ep-yellow-sun-a20bfr41.eu-central-1.aws.neon.tech/locallibrary?sslmode=require'

# To run the tests: export TESTING=1, or to use the app: unset TESTING
# TESTING = 1

# To see the current value just type echo $TESTING
if 'TESTING' in os.environ:
    db_from_env = dj_database_url.config(default=POSTGRESQL_URL, conn_max_age=500)
else:
    db_from_env = dj_database_url.config(default=NEON_URL, conn_max_age=500)
    # To use Neon with Django, you have to create a Project on Neon and specify the project connection settings in your settings.py in the same way as for standalone Postgres.

# To use Neon with Django, you have to create a Project on Neon and specify the project connection settings in your settings.py in the same way as for standalone Postgres.

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'locallibrary',
    'USER': 'ignacio.nunnez',
    'PASSWORD': 'WQjce6b7izlA',
    'HOST': 'ep-yellow-sun-a20bfr41.eu-central-1.aws.neon.tech',
    'PORT': '5432',
    'OPTIONS': {'sslmode': 'require'},
  }
}
