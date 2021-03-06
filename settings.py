# Django settings for blog project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('michal', 'michal.jedryka@gmail.com'),
)

MANAGERS = ADMINS
APP_ROOT = '/usr/src/app'

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'nspj'             # Or path to database file if using sqlite3.
DATABASE_USER = 'nspj'             # Not used with sqlite3.
DATABASE_PASSWORD = 'password'         # Not used with sqlite3.
DATABASE_HOST = 'nspj-mysql'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = '3306'             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Warsaw'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pl'

SITE_ID = 1
SITE_URL = "http://www.nspj.bydgoszcz.pl"
# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/usr/src/app/site_media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/site_media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'j^a^#)mt8^&i^e%34w8eg%_r7tid%0f-$5iglal!(_(gjb35bo'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
"django.core.context_processors.auth",
"django.core.context_processors.request",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"globs.globs",
"today.today",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
'/usr/src/app/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'news',
    'tresc',
    'treemenus',
    'tagging',
    'contact',
    'newsletter',
    'markdown',
#    'grappelli',
)

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
#EMAIL_HOST_USER = '
#EMAIL_HOST_PASSWORD = ''
#EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'michal.jedryka@gmail.com'
