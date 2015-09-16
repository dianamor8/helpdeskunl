
#encoding:utf-8
"""
Django settings for helpdeskunl project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(usi7)r_az-w+gf@7u9(892^1a)ji1cf4+sz75m83n&o_67-8)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
#PARA QUE EL USUARIO SEA MANEJADO POR PERFIL
#AUTH_PROFILE_MODULE = 'helpdeskunl.apps.usuarios.Perfil'
AUTH_USER_MODEL='usuarios.Perfil'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',    
    'helpdeskunl.apps.tiposoporte',
    'helpdeskunl.apps.incidencia',
    'helpdeskunl.apps.home',
    'helpdeskunl.apps.centro_asistencia',
    'helpdeskunl.apps.base_conocimiento',
    'helpdeskunl.apps.usuarios',
    'drealtime',
)

MIDDLEWARE_CLASSES = (
    #'django.middleware.cache.UpdateCacheMiddleware', 
    'drealtime.middleware.iShoutCookieMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',    
    'helpdeskunl.apps.home.current_user.CurrentUserMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
)

# TEMPLATE_CONTEXT_PROCESSORS = (
#     "django.contrib.auth.context_processors.auth",
#     "django.core.context_processors.debug",
#     "django.core.context_processors.i18n",
#     "django.core.context_processors.media",
#     "django.core.context_processors.static",
#     "django.core.context_processors.tz",
#     "django.contrib.messages.context_processors.messages")


ROOT_URLCONF = 'helpdeskunl.urls'

WSGI_APPLICATION = 'helpdeskunl.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'helpdeskunl',
        'USER': 'helpdeskunl',
        'PASSWORD': 'helpdeskunl',
        'HOST':'127.0.0.1',
        'PORT':'5432',
    }
}




TEMPLATE_DIRS = os.path.join(BASE_DIR,'helpdeskunl/templates'),
#os.path.join(os.path.dirname(__file__),'templates'),
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-EC'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
#

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

#SERVIDOR DE MEDIOS
MEDIA_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'helpdeskunl/media/'))
MEDIA_URL = '/media/'


#PARA DECORADOR DE LOGIN_URL
LOGIN_URL = '/login/' # HASTA MIENTRAS 11759072 25 DE MAYO 11:30 CONSULTA GENERAL. 
LOGIN_REDIRECT_URL = '/'

# MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
#CACHES = {
#    'default': {
#        'BACKEND': 'redis_cache.RedisCache',
#        'LOCATION': '127.0.0.1:6379',
#    # 'LOCATION': '/var/run/redis/redis.sock',
#    # 'OPTIONS': {
#    #     'DB': 1,
#    #     'PASSWORD': <password-de-redis>
#    #     },
#   },
#}



