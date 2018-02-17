# Copyright 2018 Mathew Robinson <chasinglogic@gmail.com>. All rights reserved.
# Use of this source code is governed by the AGPLv3 license that can be found in
# the LICENSE file.

"""
Django settings for the praelatus project.
"""

import sys
import os

from os.path import abspath, basename, dirname, join, normpath

from praelatus.settings.env import CONFIG
from praelatus.celery import app as celery_app
__all__ = ['celery_app']

#### PROJECT SETTINGS, NOT CONFIGURABLE ###################

RELEASE_NAME = 'Rio Bravo'
VERSION = '0.1.0'

APPEND_SLASH = False

###### PATH CONFIGURATION ################################

# fetch Django's project directory
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# fetch the project_root
PROJECT_ROOT = dirname(DJANGO_ROOT)
DATA_DIR = os.getenv('PRAELATUS_DATA_DIR ', join(PROJECT_ROOT, 'data'))
if not os.path.isdir(DATA_DIR):
    os.mkdir(DATA_DIR)

# the name of the whole site
SITE_NAME = 'praelatus'

# collect static files here
STATIC_ROOT = join(DATA_DIR, 'static')
# collect media files here
MEDIA_ROOT = join(DATA_DIR, 'static', 'media')

STATICFILES_DIR = [
    join(PROJECT_ROOT, 'static')
]

# serve static files from
STATIC_URL = '/static/'

# look for templates here
# This is an internal setting, used in the TEMPLATES directive
PROJECT_TEMPLATES = [
    join(PROJECT_ROOT, 'templates'),
]

# add apps/ to the Python path
sys.path.append(normpath(join(PROJECT_ROOT, 'apps')))

INSTALLED_APPS = [
    # Row level security
    'guardian',
    # Filtering of models
    'django_filters',
    # REST API
    'rest_framework',
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Praelatus
    'projects.apps.ProjectsConfig',
    'tickets.apps.TicketsConfig',
    'notifications.apps.NotificationsConfig',
    'profiles.apps.ProfilesConfig',
    'queries.apps.QueriesConfig',
    'schemes.apps.SchemesConfig',
    'workflows.apps.WorkflowsConfig',
    'labels.apps.LabelsConfig',
    'fields.apps.FieldsConfig'
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'praelatus.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': ['templates'],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

WSGI_APPLICATION = 'praelatus.wsgi.application'

REST_FRAMEWORK = {
    # Integrate Django Filters
    'DEFAULT_FILTER_BACKENDS':
    ('django_filters.rest_framework.DjangoFilterBackend', ),

    # Use sessions or basic auth
    'DEFAULT_AUTHENTICATION_CLASSES':
    ('rest_framework.authentication.BasicAuthentication',
     'rest_framework.authentication.SessionAuthentication', ),

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES':
    ['rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly']
}


X_FRAME_OPTIONS = 'DENY'

### AUTHENTICATION #####
# SECURITY WARNING: keep the secret key used in production secret!
if os.path.exists(os.path.join(DATA_DIR, '.secret_key')):
    with open(os.path.join(DATA_DIR, '.secret_key')) as f:
        SECRET_KEY = f.read()
else:
    with open(os.path.join(DATA_DIR, '.secret_key'), 'w') as f:
        import binascii
        rand = os.urandom(128)
        SECRET_KEY = binascii.b2a_hex(rand).decode('ascii')
        f.write(SECRET_KEY)

LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/tickets/dashboard'
LOGOUT_REDIRECT_URL = '/'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_PROFILE_MODULE = 'profiles.Profile'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'projects.backends.ObjectPermissionAnonFallbackBackend',
    'guardian.backends.ObjectPermissionBackend'
)

CONFIG['media_root'] = os.getenv(
    'PRAE_MEDIA_ROOT', join(DATA_DIR, 'media')),

if CONFIG.get('https', False):
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONFIG.get('debug', False)
ALLOWED_HOSTS = CONFIG.get('allowed_hosts', ['localhost'])
SESSION_ENGINE = CONFIG.get('session_engine')
DATABASES = CONFIG.get('database')

# Internationalization
LANGUAGE_CODE = CONFIG.get('language_code')
TIME_ZONE = CONFIG.get('time_zone')
USE_I18N = CONFIG.get('use_i18n')
USE_TZ = CONFIG.get('use_tz')

STATIC_ROOT = CONFIG.get('static_root', STATIC_ROOT)
MEDIA_ROOT = CONFIG.get('media_root', MEDIA_ROOT)

# CACHING

CACHES = CONFIG.get('cache')

# CELERY

CELERY_BROKER_URL = CONFIG.get('mq_server')
CELERY_RESULT_BACKEND = CONFIG.get('mq_result_backend')

# EMAIL

EMAIL_BACKEND = CONFIG.get('email', {}).get('backend')
EMAIL_ADDRESS = CONFIG.get('email', {}).get('address')
EMAIL_HOST = CONFIG.get('email', {}).get('host')
EMAIL_PORT = CONFIG.get('email', {}).get('port')
EMAIL_HOST_USER = CONFIG.get('email', {}).get('username')
EMAIL_HOST_PASS = CONFIG.get('email', {}).get('password')
EMAIL_USE_TLS = CONFIG.get('email', {}).get('use_tls')
EMAIL_USE_SSL = CONFIG.get('email', {}).get('use_ssl')
