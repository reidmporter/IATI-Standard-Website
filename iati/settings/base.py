"""Django settings for iati project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url

# Mark language names as translation strings
from django.utils.translation import gettext_lazy as _

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

ADMINS = (
    ('Russell Kirkland', 'russell@mashandgravy.co.uk'),
)

SECRET_KEY = 'enter-a-long-unguessable-string-here'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    'wagtail_modeltranslation',
    'wagtail_modeltranslation.makemigrations',
    'wagtail_modeltranslation.migrate',
    'home',
    'search',
    'about',
    'contact',
    'events',
    'guidance_and_support',
    'news',
    'iati_standard',
    'using_data',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',

    'modelcluster',
    'taggit',
    'haystack',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'wagtail.contrib.search_promotions',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',

    'modeltranslation_sync',
    'django_extensions',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    # For determining browser locale, must come after sessions and cache (not present) and before common
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'iati.custom_middleware.RedirectIATISites',
    'iati.custom_middleware.LowercaseMiddleware',
]

ROOT_URLCONF = 'iati.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'iati.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config()
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', _('English')),
    ('fr', _('French')),
    ('es', _('Spanish')),
    ('pt', _('Portuguese')),
]

ACTIVE_LANGUAGES = [
    ('en', _('English')),
    ('fr', _('French')),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'home/static'),
    os.path.join(BASE_DIR, 'patterns/converted-html/assets'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/assets/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

DOCUMENTS_SLUG = 'documents'
DOCUMENTS_URL = '/{}/'.format(DOCUMENTS_SLUG)

ADMIN_SLUG = 'cms'
ADMIN_URL = '/{}/'.format(ADMIN_SLUG)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Wagtail settings

WAGTAIL_SITE_NAME = "iati"


# Reference namespaces for URL redirection
REFERENCE_NAMESPACES = [
    "101",
    "102",
    "103",
    "104",
    "105",
    "201",
    "202",
    "203",
    "activity-standard",
    "codelists",
    "developer",
    "introduction",
    "namespaces-extensions",
    "organisation-identifiers",
    "organisation-standard",
    "reference",
    "rulesets",
    "schema",
    "upgrades",
    "guidance/datastore",
]

REFERENCE_REDIRECT_BASE_URL = 'http://reference.iatistandard.org'

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://iatistandard.org'

# Modeltranslation sync Settings
MODELTRANSLATION_LOCALE_PATH = os.path.join(BASE_DIR, 'locale')
LOCALE_PATHS = (MODELTRANSLATION_LOCALE_PATH,)
MODELTRANSLATION_PO_FILE = "iati.po"

ZENDESK_REQUEST_URL = 'https://iati.zendesk.com/api/v2/requests.json'

# Community URL
COMMUNITY_URL = 'https://discuss.iatistandard.org/'

# Social Media
TWITTER_HANDLE = 'IATI_aid'
YOUTUBE_CHANNEL_URL = 'https://www.youtube.com/channel/UCAVH1gcgJXElsj8ENC-bDQQ'

# Relative URL for the default social media sharing image
DEFAULT_SHARE_IMAGE_URL = 'img/iati-share-social.png'


# Search settings
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.elasticsearch2',
        'URLS': [os.getenv('ELASTICSEARCH_URL', 'http://localhost:9200')],
        'INDEX': 'iati',
    },
}

HAYSTACK_CONNECTIONS = {
    'default': {},
}

HAYSTACK_CUSTOM_HIGHLIGHTER = 'search.utils.CustomHighlighter'
