import os
from django.conf import settings

DATABASES = settings.DATABASES

DEBUG = False
TEMPLATE_DEBUG = False

# Parse database configuration from $DATABASE_URL

import dj_database_url
DATABASES = {
    "default": dj_database_url.config(default='postgres://localhost'),
}

DATABASES['default']['CONN_MAX_AGE'] = 500



STATICFILE_STORAGE = 'whitenoise.django.GzipManifestSTaticFilesStorage'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
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

INSTALLED_APPS = (
    'admin_tools.theming',
    'admin_tools.menu',
    'autocomplete_light',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'jquery',
    'project',
    'pinax_theme_bootstrap',
    'bootstrapform',
    'haystack',
    'imagestore',
    'sorl.thumbnail',
    'tagging',
    'follow',
    'easy_thumbnails',
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
    'djrill',
)
