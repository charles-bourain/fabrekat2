import os
from django.conf import settings

DATABASES = settings.DATABASES

import os
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DEBUG = False
TEMPLATE_DEBUG = False

# Parse database configuration from $DATABASE_URL

import dj_database_url
DATABASES = {
    "default": dj_database_url.config(default='postgres://localhost'),
}

DATABASES['default']['CONN_MAX_AGE'] = 500



STATICFILE_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
        }
    }
}


MANDRILL_API_KEY = "3rxHtBbmRLBbLi4EgazU-A"
EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
DEFAULT_FROM_EMAIL = "webmaster@fabrekat.com"


TEMPLATE_DIRS=(
    os.path.join(BASE_DIR, 'templates'),
    )

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
LOGIN_URL = '/account/login/'


INSTALLED_APPS = (
    'django.contrib.auth',
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'jquery',
    'project',
    'pinax_theme_bootstrap',
    'bootstrapform',
    'tagging',
    'follow',
    'publishedprojects',
    'projectpricer',
    'projecttags',
    'debug_toolbar',
    'bottlenose',
    'mathfilters',
    'registration',
    'designprofiles',
    'projectsteps',
    'widget_tweaks',
    'crispy_forms',
    'imagestore',
    'djrill',
    'whitenoise',
)
