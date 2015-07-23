# coding: utf-8
from django.utils.translation import ugettext_lazy as _


DEBUG = True
ALLOWED_HOSTS = ['*',]
TIME_ZONE = 'Asia/Chongqing'
LANGUAGE_CODE = 'zh-hans'
USE_I18N = True
USE_L10N = True
USE_THOUSAND_SEPARATOR = True


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'bootstrap3',
    'inface.uc',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'inface',                      # Or path to database file if using sqlite3.
        'USER': 'postgres',                      # Not used with sqlite3.
        'PASSWORD': 'qqqqqq',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['D:/webprojects/inface/templates',],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.i18n',
                ],
            },
        },
    ]

STATICFILES_DIRS = (
    ("css", "d:/webprojects/inface/static/css"),
    ("js", "d:/webprojects/inface/static/js"),
    ("images", "d:/webprojects/inface/static/images"),
)

# LoginView
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/home/'
AUTH_USER_MODEL = 'uc.MyUser'

#static url
STATIC_URL = 'http://inface.inportal.cn/static/'

#media url
MEDIA_ROOT = 'D:/webprojects/inface/media/'
MEDIA_URL = 'http://office.scotsuka.com/media/'

LOCALE_PATHS = (
    'D:/webprojects/inface/locale',
)
LANGUAGES = (
    ('zh-hans', _(u'Chinese')),
    ('en', _(u'English')),
)




