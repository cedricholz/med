"""
Django settings for med project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import mimetypes
import os
from datetime import timedelta
from pathlib import Path

import boto3
import sentry_sdk
from decouple import config
from sentry_sdk.integrations.django import DjangoIntegration

mimetypes.add_type("text/javascript", ".js", True)
ENV = config("ENV", None)
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", "TESTING")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_URL = '/static/'
STATIC_ROOT = "static"

AWS_REGION_NAME = 'us-west-1'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'frontend/build/static'),
)
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# AWS_PRELOAD_METADATA = True
# AWS_QUERYSTRING_AUTH = False

AWS_DEFAULT_ACL = None
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

# AWS_S3_FILE_OVERWRITE = False


STORAGES = {
    "default": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    }
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)
# DEBUG = False

if ENV == 'production':

    ssm = boto3.client(
        "ssm",
        region_name=AWS_REGION_NAME,
    )

    next_token = None
    parameters = []
    while True:
        path = f"/"

        if next_token:
            response = ssm.get_parameters_by_path(
                Path=path,
                WithDecryption=True,
                NextToken=next_token,
            )
        else:
            response = ssm.get_parameters_by_path(
                Path=path,
                WithDecryption=True,
            )

        for param in response.get("Parameters"):
            name = param.get("Name").lstrip(path)
            os.environ.setdefault(name, param.get("Value"))

        next_token = response.get("NextToken")
        if not next_token:
            break
    SECRET_KEY = config("SECRET_KEY", "")
    print("Loaded SSM parameters")


AWS_PUBLIC_BUCKET = "med-files"
DREAMSHIP_API_KEY = config("DREAMSHIP_API_KEY", "")
SENDGRID_API_KEY = config("SENDGRID_API_KEY", "")

if ENV == 'production':
    STRIPE_SECRET_KEY = config("STRIPE_PROD_SECRET_KEY", "")
    STRIPE_PUBLISHABLE_KEY = config("STRIPE_PROD_PUBLISHABLE_KEY", "")
    WEBHOOK_URL = 'https://marlin.surf/webhooks/'
    REDIRECT_URL = 'https://marlin.surf/redirects/'
    SITE_URL = 'https://marlin.surf/'
else:
    STRIPE_SECRET_KEY = config("STRIPE_DEV_SECRET_KEY", "")
    STRIPE_PUBLISHABLE_KEY = config("STRIPE_DEV_PUBLISHABLE_KEY", "")
    WEBHOOK_URL = 'https://ds-cedric.ngrok.io/webhooks/'
    REDIRECT_URL = 'https://ds-cedric.ngrok.io/redirects/'
    SITE_URL = 'https://ds-cedric.ngrok.io/'

MAIN_EMAIL = 'marlin@marlin.surf'
MAIL_PHONE = '+18054487693'

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", "")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    "webpack_loader",
    "med",
    "file",
    "site_configuration",
    "django_extensions",
]
ROOT_URLCONF = "med.urls"
CSRF_COOKIE_NAME = 'csrftoken'
CORS_ALLOW_CREDENTIALS = True

if ENV == "production":
    # ALLOWED_HOSTS = [
    #     'marlin.surf',
    #     '*.marlin.surf',
    #     'd13hr3th4mibef.cloudfront.net',
    #     'marlinsurf-environment.eba-emyfxezg.us-west-1.elasticbeanstalk.com',
    #     'awseb-awseb-125uuj5l0cu5p-1022834688.us-west-1.elb.amazonaws.com',
    #     '.elasticbeanstalk.com',
    # ]
    ALLOWED_HOSTS = [
        "172.31.26.248",
        "marlin.surf",
        "staging.marlin.surf",
    ]
else:
    ALLOWED_HOSTS = [
        'localhost',
        '127.0.0.1',
        'ds-cedric.ngrok.io',
    ]

CORS_ALLOWED_ORIGINS = [
    "https://marlin.surf",
    "https://staging.marlin.surf",
    "http://d13hr3th4mibef.cloudfront.net",
    "https://d13hr3th4mibef.cloudfront.net",
    "https://marlinsurf-environment.eba-emyfxezg.us-west-1.elasticbeanstalk.com",
    "http://marlinsurf-environment.eba-emyfxezg.us-west-1.elasticbeanstalk.com",
]

# TWILIO_SID = config("TWILIO_SID")
# TWILIO_AUTH_TOKEN = config("TWILIO_AUTH_TOKEN")

if ENV == "production":
    CORS_ORIGIN_WHITELIST = [
        "marlin.surf",
        "*.marlin.surf",
        "d13hr3th4mibef.cloudfront.net",
        "marlinsurf-environment.eba-emyfxezg.us-west-1.elasticbeanstalk.com",
    ]
else:
    CORS_ORIGIN_WHITELIST = [
        'https://ds-cedric.ngrok.io',
        'http://localhost:3000',
        'http://localhost:8000',
        'http://localhost:8000',
        'http://127.0.0.1:8000',
        'http://127.0.0.1:3000',
    ]

class PrintHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request.META['HTTP_HOST'])
        return self.get_response(request)

MIDDLEWARE = [
    'med.settings.PrintHostMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    "DEFAULT_TIMEOUT": 300,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True
}
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [os.path.join(BASE_DIR, 'frontend/build')],
        # 'DIRS': [os.path.join(BASE_DIR, 'frontend/public')],
        # 'DIRS': [os.path.join(BASE_DIR, 'build')],
        # 'DIRS': [os.path.join(BASE_DIR, 'marlinsurf/templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "med.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if ENV == "production":
    # DATABASES = {
    #     "default": {
    #         "ENGINE": "django.db.backends.postgresql",
    #         "NAME": "",
    #         "USER": "postgres",
    #         "PASSWORD": config("DATABASE_PASSWORD", ""),
    #         "HOST": "marlinsurf-db.cv3vzyq2vtbc.us-west-1.rds.amazonaws.com",
    #         "PORT": "5432",
    #     },
    # }
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config("RDS_DB_NAME"),
            'USER': config('RDS_USERNAME'),
            'PASSWORD': config('RDS_PASSWORD'),
            'HOST': config('RDS_HOSTNAME'),
            'PORT': config('RDS_PORT'),
        }
    }

elif config("ENV") == 'development':
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "med",
            "USER": config("LOCAL_USER_NAME", ""),
            "PASSWORD": config("LOCAL_PASSWORD", ""),
            "HOST": "localhost",
            "PORT": "5432",
        },
    }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# STATIC_URL = "static/"


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': '/',
        'STATS_FILE': os.path.join(BASE_DIR, 'frontend/webpack-stats.json'),
    }
}
if config("ENV") != 'development':
    sentry_sdk.init(
        dsn="https://db0ec4beaf1c499bbea6594590295d67@o4505469855334400.ingest.sentry.io/4505469857628160",
        integrations=[
            DjangoIntegration(),
        ],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )
