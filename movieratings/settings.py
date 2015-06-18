"""
Django settings for movieratings project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v+0(u(5a4-_!$*q%z))h8#0iyrnioe8179dvkvl=bmd0(063y$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#TEMPLATE_DEBUG = False # comment out if not in production

ALLOWED_HOSTS = ['.herokuapp.com','.127.0.0.1']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Rater',

#    'debug_toolbar',
#    'django_extensions',
    'bootstrap3',
#    'updates',
#    'users',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'movieratings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'movieratings.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# Parse database configuration from $DATABASE_URL
#print(os.environ.get('DATABASE_URL', None))
#if os.environ.get('DATABASE_URL', None):
import dj_database_url
DATABASES = {}
DATABASES['default'] = dj_database_url.config()
#else:
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #         'NAME': 'pdb',
    #         'USER': 'pdb',
    #         'HOST': '127.0.0.1'
    # #        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #     },
    # }


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# To create PostgreSQL db:
# > createuser mowdie
# > createdb -U mowdie mowdie
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'mowdie',
#         'USER': 'mowdie',
#         'HOST': '127.0.0.1',
#     },
# }


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
STATIC_ROOT = os.path.join(BASE_DIR, "project_static")

LOGIN_REDIRECT_URL = '../index.html'

# Bootstrap

BOOTSTRAP3 = {

    # The URL to the jQuery JavaScript file
    'jquery_url': '/static/jquery-2.1.4.min.js',

    # The Bootstrap base URL
    'base_url': '/static/bootstrap/',

    # The complete URL to the Bootstrap CSS file (None means no theme)
#    'theme_url': '/static/bootstrap/css/sandstone.css',
    'theme_url': '/static/bootstrap/css/bootstrap-theme.min.css',

    # Include jQuery with Bootstrap JavaScript (affects django-bootstrap3 template tags)
    'include_jquery': True,
}

ADMINS = (
    ('Alan Rominger', 'alan.rominger@gmail.com')
)


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
if os.environ.get('DATABASE_URL', None):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_ROOT = 'staticfiles'
    STATIC_URL = '/static/'

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
    )
