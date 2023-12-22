from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-53ypxv-m%weh%&6b40z)+z0i#4xz^e1_6pdqe(ez1g#*i4v=08'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
AUTH_USER_MODEL = 'novusapp.CustomUser'
# LOGIN_URL = 'login_view'
# LOGIN_REDIRECT_URL = 'dashboard_redirect'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
from django.contrib import messages
MESSAGE_TAGS = {
    messages.DEBUG: 'primary',   # Bootstrap class: 'primary'
    messages.INFO: 'info',      # Bootstrap class: 'info'
    messages.SUCCESS: 'success',# Bootstrap class: 'success'
    messages.WARNING: 'warning',# Bootstrap class: 'warning'
    messages.ERROR: 'danger',   # Bootstrap class: 'danger'
}


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'novusapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]




# settings.py

# Set session timeout to 30 days (30 days * 24 hours * 60 minutes * 60 seconds)
SESSION_COOKIE_AGE = 2592000


ROOT_URLCONF = 'novusproject.urls'
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'novusapp.context_processors.add_username_to_context',           
            ],
        },
    },
]

WSGI_APPLICATION = 'novusproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
import yaml
credentials = yaml.load(open('./novusproject/credentials.yml','r'),Loader=yaml.FullLoader)

db_name = credentials['db_name']
user = credentials['user']
password = credentials['password']
host = credentials['host']
port = credentials['port']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': db_name,
        'USER': user,
        'PASSWORD': password,
        'HOST' : host,
        'PORT': port,
        
        
    }
}
# DATABASE_DIR = os.path.join(BASE_DIR, 'db.sqlite3')
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': DATABASE_DIR,
#     }
# }

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


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ankit.sharma@novusinsights.com'
EMAIL_HOST_PASSWORD = ''

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]


PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]



# JAZZMIN_SETTINGS = {
#     "site title": "Novus Log Administrator",
#     "site_logo": "images/novus_logo.png",
#     "site_brand": "Novus Admin",
#     "copyright": "Novus Insights Ltd",
#     "site_logo_classes": "img-circle",
#     "welcome_sign": "Welcome to the Novus Admin",

#     # "topmenu_links": [

#     #     # Url that gets reversed (Permissions can be added)
#     #     {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},

#     #     # external url that opens in a new window (Permissions can be added)
#     #     {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},

#     #     # model admin to link to (Permissions checked against model)
#     #     {"model": "auth.User"},

#     #     # App with dropdown menu to all its models pages (Permissions checked against models)
#     #     {"app": "CustomUser"},
#     # ],


    

    
    
# }
# JAZZMIN_SETTINGS["show_ui_builder"] = True 