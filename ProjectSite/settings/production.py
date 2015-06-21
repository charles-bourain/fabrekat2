import os
from django.conf import settings

DATABASES = settings.DATABASES

DEBUG = False
TEMPLATE_DEBUG = False

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
# import os
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# STATIC_ROOT = 'staticfiles'
# STATIC_URL = '/static/'

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )

INSTALLED_APPS = (
    # 'django_admin_bootstrapped',
    'admin_tools.theming',
    'admin_tools.menu',
    # 'admin_tools.dashboard',
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
    'account',
    'pinax_theme_bootstrap',
    'bootstrapform',
    'haystack',
    'imagestore',
    'sorl.thumbnail',
    'tagging',
    'follow',
    'easy_thumbnails',
    # 'fabricator',
    'publishedprojects',
    # 'geoposition',
    'projectpricer',
    'projectcatagories',
    #'debug_toolbar',
)