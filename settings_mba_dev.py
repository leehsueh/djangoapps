# DEVELOPMENT settings
# Django settings for siteapps_v1 project.

DEBUG = True
PRNT_STMT = True
TEMPLATE_DEBUG = DEBUG
USE_DEPLOYED_DB = False

ADMINS = (
    # ('Hain-Lee', 'leehsueh7@gmail.com'),
)

MANAGERS = ADMINS

# Database settings
if not USE_DEPLOYED_DB:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'leehsueh_djangoapps',
            'USER': 'leehsueh',
            'PASSWORD': 'djangoapps',
            'HOST': '',
            'PORT': '',
        },

    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'leehsueh_appsv1',
            'USER': 'leehsueh_appsv1',
            'PASSWORD': 'trunksu',
            'HOST': 'web110.webfaction.com',
            'PORT': '5432',
        }
    }


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1
SITE_URL = "http://tjcbdb.info"

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/Users/leehsueh7/Code/siteapps_v1/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin/media/'

# Absolute path to the directory that holds static files.
# Example: "/home/static/static.lawrence.com/"
#STATIC_ROOT = 'c://Users//leehsueh//webdev//gitstuff//siteapps_v1//static//'

# URL that handles the media served from STATIC_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
STATIC_URL = '/static/'

STATICFILES_DIRS = ('/Users/leehsueh7/Code/siteapps_v1/static/',)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django.contrib.staticfiles.finders.FileSystemFinder",
)
    
LOGIN_URL = '/accounts/login/'
    
# Make this unique, and don't share it with anybody.
SECRET_KEY = 'u%828kd-+1o6xe!$bx!*rllw+uj8#g!05c%c3r_bs8d2kv#pt!'

# Biblia API key
BIBLIA_API_KEY = 'd43cf9c9e02a3f4187e917a0e4f682a1'

TEMPLATE_CONTEXT_PROCESSORS =  ("django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 1209600/4
ROOT_URLCONF = 'siteapps_v1.urls'

import os.path

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__),'templates').replace('\\','/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.comments',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'siteapps_v1.bibledb',
    'siteapps_v1.ntgreekvocab',
    'siteapps_v1.bible_tidbits',
)

EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'leehsueh_tjcbdb'
EMAIL_HOST_PASSWORD = 'B@&f@ction'
DEFAULT_FROM_EMAIL = 'admin@tjcbdb.info'
SERVER_EMAIL = 'admin@tjcbdb.info'
