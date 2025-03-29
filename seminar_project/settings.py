import os
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
# keta haluha muda mos DATABASE
BASE_DIR_DB = Path(__file__).resolve().parent.parent


# Media settings
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, "static")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f2tn=4k@nrv$yqkkt@k+-b33=8ef*-$bz+!llir#5=3qzscl8z'

# SECURITY WARNING: don't run with debug turned on in production!

# keta haluha muda mos DATABASE
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Media Files (for uploads)
MEDIA_URL = "/media/"  # URL path for media files
MEDIA_ROOT = os.path.join(BASE_DIR_DB, "media")  # Where uploaded files are stored


DEBUG = True

ALLOWED_HOSTS = ["localhost"]
CSRF_TRUSTED_ORIGINS = [
    "http://#"
]
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'seminar',
    'rejistu',
    'facer',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


GOOGLE_MAPS_API_KEY = ""


# Serve static files with WhiteNoise
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

ROOT_URLCONF = 'seminar_project.urls'

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

WSGI_APPLICATION = 'seminar_project.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'NAME': BASE_DIR_DB / 'db.sqlite3',
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
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# Static Files (for CSS, JS, images)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")  # Ensure this is defined
# STATICFILES_DIRS = [os.path.join(BASE_DIR, "staticfiles")]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
