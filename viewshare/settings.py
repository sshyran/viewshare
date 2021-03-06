from os import path
from posixpath import join as url_join
from imp import find_module

DEBUG = True
TEMPLATE_DEBUG = DEBUG
REQUIRE_DEBUG = DEBUG

ADMINS = (
# ('Your Name', 'your_email@domain.com'),
)
MEDIA_ROOT = path.join(path.dirname(__file__), '..', "media")
MEDIA_URL = '/media/'

STATIC_ROOT = path.join(path.dirname(__file__), '..', "static")
STATIC_URL = '/static/'

FILE_UPLOAD_PATH = path.join(path.dirname(__file__), '..', "upload")

COMPRESS_ROOT = STATIC_ROOT
COMPRESS_URL = STATIC_URL

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dev.db', # Or path to database file if using sqlite3.
        'USER': '', # Not used with sqlite3.
        'PASSWORD': '', # Not used with sqlite3.
        'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
        'ATOMIC_REQUESTS': True,
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'US/Eastern'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True


# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = url_join(STATIC_URL, "admin/")

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'changeme'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'django.middleware.transaction.TransactionMiddleware',

    )

ROOT_URLCONF = 'viewshare.urls'

AUTHENTICATION_BACKENDS = (
    'viewshare.apps.exhibit.permissions.RegistryBackend',
    'django.contrib.auth.backends.ModelBackend',
    )

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    'django.contrib.messages.context_processors.messages',
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    "viewshare.utilities.context_processors.viewshare_settings",
    "viewshare.apps.vendor.notification.context_processors.notification",
    "viewshare.apps.connections.context_processors.invitations",
    )

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    # included
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.humanize',
    #'django.contrib.markup',
    'django.contrib.admin',

    # external
    'djcelery',
    'django_extensions',
    'pagination',
    'crispy_forms',
    'compressor',
    'south',
    'require',
    'django_gravatar',

    # Freemix specific
    'viewshare.utilities',
    'viewshare.apps.legacy.dataset',
    'viewshare.apps.exhibit',
    'viewshare.apps.augment',
    'viewshare.apps.share',

    # Viewshare specific
    'viewshare.apps.vendor.notification',
    'viewshare.apps.vendor.friends',
    'announcements',

    'viewshare.apps.account',
    'viewshare.apps.discover',
    'viewshare.apps.profiles',
    'viewshare.apps.connections',
    'viewshare.apps.upload',

    # Support pipeline
    'viewshare.apps.support',

    # Site registration
    'registration',
    'viewshare.apps.moderated_registration',
    )

module_path = lambda m: path.abspath(find_module(m)[1])

STATICFILES_DIRS = (path.join(module_path('viewshare'), 'static'),)

ABSOLUTE_URL_OVERRIDES = {
    "auth.user": lambda o: "/profiles/profile/%s/" % o.username,
}
AUTH_PROFILE_MODULE = 'profiles.Profile'
NOTIFICATION_LANGUAGE_MODULE = 'account.Account'

TEMPLATE_DIRS = (
    path.join(module_path("viewshare"), "templates"),
    )

# Set to describe the site, properties and the names

SITE_NAME = "Viewshare"
SITE_NAME_STATUS = "BETA"
CONTACT_EMAIL = "noreply@example.com"

LOGIN_URL = "/account/login"
LOGIN_REDIRECT_URLNAME = "user_home"

ANONYMOUS_USERNAME = 'guest'

ACCOUNT_REQUIRED_EMAIL = False
ACCOUNT_EMAIL_VERIFICATION = False

ACCOUNT_ACTIVATION_DAYS = 14

FIXTURE_DIRS = (
    path.join(module_path("viewshare"), "fixtures"),
    )

# Javascript and CSS compression
COMPRESS_ENABLED = False

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
    )

STATICFILES_STORAGE = 'require.storage.OptimizedStaticFilesStorage'

REQUIRE_BASE_URL = '.'

REQUIRE_JS = 'freemix/js/lib/require.js'

REQUIRE_STANDALONE_MODULES = {
        'editor-main': {
            'out': 'editor-built.js',
            'build_profile': 'editor-build.js'
        },
        'exhibit-layout-main': {
            'out': 'exhibit-layout-built.js',
            'build_profile': 'exhibit-layout-build.js'
        },
        'exhibit-display-main': {
            'out': 'exhibit-display-built.js',
            'build_profile': 'exhibit-display-build.js'
        },
        'embed-main': {
            'out': 'embed-built.js',
            'build_profile': 'embed-build.js'
        }
}

REQUIRE_DEBUG = DEBUG

CRISPY_TEMPLATE_PACK = 'bootstrap'

GRAVATAR_DEFAULT_IMAGE = 'identicon'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Validate the request's Host header and protect
# against host-poisoning attacks
ALLOWED_HOSTS = ('viewshare.org', )

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CELERY_ALWAYS_EAGER = True

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'freemix': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
        'viewshare': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
        'django': {
            'handlers': ['console'],
            'level': 'ERROR'
        }
    }
}

LOCAL_INSTALLED_APPS = ()

try:
    from local_settings import *
except ImportError:
    pass

INSTALLED_APPS += LOCAL_INSTALLED_APPS

import djcelery
djcelery.setup_loader()
