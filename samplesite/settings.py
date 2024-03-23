"""
Django settings for samplesite project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import environ
env = environ.Env()
environ.Env.read_env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bboard.apps.BboardConfig',
    'accounts.apps.AccountsConfig',
    'django.contrib.postgres',
    'captcha',
    'precise_bbcode',
    "bootstrap4",
]

MIDDLEWARE = [
    # 'django.middleware.http.ConditionalGetMiddleware', #для кэша на стороне пользователя
    'django.middleware.security.SecurityMiddleware',

    # 'django.middleware.cache.UpdateCacheMiddleware', #для кэша
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    # 'django.middleware.cache.FetchFromCacheMiddleware', #для кэша

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'bboard.middlewares.my_middleware',
    # 'bboard.middlewares.RubricMiddleware'
]

ROOT_URLCONF = 'samplesite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth', #данные о User. Можно узнать что пользователь залогирован. User.is_authentificated

                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
                'bboard.middlewares.rubrics'
            ],
        },
    },
]

WSGI_APPLICATION = 'samplesite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        # 'ATOMIC_REQUEST': False,
        # 'AUTOCOMMIT': False,
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        # 'OPTIONS': '',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'samplesite.validators.NoForbiddenCharsValidator',
        'OPTIONS': {'forbidden_chars': (' ', ',', '.')},
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Asia/Almaty'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

CAPTHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'
CAPTCHA_LENGTH = 4
CAPTCHA_WORDS_DICTIONARY = '/static/words.txt'
CAPTCHA_TIMEOUT = 5


#BBcode
BBCODE_NEWLINE = "<br>"

BOOTSTRAP4 = {
    'horizontal_label_class': "col-md-3",
    'horizontal_field_class': "col-md-9",
    'required_css_class': "",
    'success_css_class': "has-success",
    'error_css_class': "has-error",
}

# SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# SESSION_ENGINE = 'django.contrib.sessions.backends.file'
# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
# SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
# SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

# from django.contrib import messages
# MESSAGE_LEVEL = messages.DEBUG
# MESSAGE_TAGS =

# DEBUG = 10
# INFO = 20
# SUCCESS = 25
# WARNING = 30
# ERROR = 40

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
# EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"


DEFAULT_FROM_EMAIL = "superdev@mail.ru"

# только для smtp
EMAIL_HOST = "sandbox.smtp.mailtrap.io"
EMAIL_PORT = '2525'
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_TIMEOUT = 60 # В СЕКУНДАХ

EMAIL_FILE_PATH = 'tmp/messages/'

ADMINS = [
    ('admin', 'admin2')
]

# MANAGERS = [
#     ('manager')
# ]

CACHES = {
    "default": {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    # "myredis": {
    #     "BACKEND": "django_redis.cache.RedisCache",
    #     "LOCATION": "redis://127.0.0.1:6379/2",
    #     "OPTIONS": {
    #         "CLIENT_CLASS": "django_redis.client.DefaultClient",
    #         "username": "kvy",
    #         "password": "QAZqaz911+",
    #     }
    # }

    #     # 'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
    #     # 'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
    #     # 'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    #     # 'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
    # },
    # 'special': {
    #     'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    #     'LOCATION': 'cache2',
}

# CACHE_MIDDLEWARE_ALIAS = 'default'
# CACHE_MIDDLEWARE_SECONDS = 600 #сек

# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'