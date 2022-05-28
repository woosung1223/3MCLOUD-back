"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path

# secret key 처리부분 import
import os, json
from django.core.exceptions import ImproperlyConfigured

# secret key 처리부분 import 종료
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'authentication.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authentication',
    'file',
    'rest_framework',
    "corsheaders", # CORS
]


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django.middleware.common.CommonMiddleware",
]
# CORS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True



ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
# STATIC_ROOT =  os.path.join(BASE_DIR, 'static')

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'  # 기본 스토리지 설정
AWS_S3_SECURE_URLS = False       # https 사용 여부
AWS_QUERYSTRING_AUTH = False     # 요청에 대한 복잡한 인증 관련 쿼리 매개 변수 허용 여부 -> 확인


###<-- 환경변수 처리부분 -->###
secret_file = os.path.join(BASE_DIR, 'secrets.json') 

with open(secret_file, 'r') as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


REGION = get_secret('region')
USER_POOL_ID = get_secret('user_pool_id')
APP_CLIENT_ID = get_secret('app_client_id')
IDENTITY_POOL_ID = get_secret('identity_pool_id')
ACCOUNT_ID = get_secret('account_id')
AWS_ACCESS_KEY = get_secret('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = get_secret('AWS_SECRET_ACCESS_KEY')
SECRET_KEY = get_secret('DJANGO_SECRET_KEY')
AWS_STORAGE_BUCKET_NAME = get_secret('AWS_STORAGE_BUCKET_NAME')  # 버킷 이름


###<-- 환경변수 처리부분 종료 -->###

AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME, REGION)
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400',} #  HTTP 응답이 재사용 가능하기 전에 다음 86400초 동안 캐시된 복사본으로 브라우저에 남아 있음

# AWS_LOCATION = 'static'
# STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
## STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] #static 폴더에 파일 저장

# static 파일 연결은 나중에 -> 장고에서 기본으로 제공하는 css가 사라짐
