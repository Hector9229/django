"""
Django settings for the tienda_online project.

Proyecto: Tienda Online API
Práctica 4 - Backend con Django, DRF, usuarios personalizados y JWT.
"""

import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# =============================================================================
# Seguridad
# =============================================================================
# En producción la SECRET_KEY debe venir de una variable de entorno.
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-_(ncxd$#1rxfz=g2=*pk=ff_7n!&dkio0h-w06$x*i34cj1tc2',
)

DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# =============================================================================
# Aplicaciones
# =============================================================================
BASE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',
    'django_filters',
]

OWN_APPS = [
    'users',
    'products',
]

INSTALLED_APPS = BASE_APPS + THIRD_APPS + OWN_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tienda_online.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tienda_online.wsgi.application'


# =============================================================================
# Base de datos
# =============================================================================
# Se usa SQLite para que el proyecto sea portable. El archivo db.sqlite3
# está excluido en .gitignore.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# =============================================================================
# Modelo de usuario personalizado
# =============================================================================
AUTH_USER_MODEL = 'users.User'


# =============================================================================
# Validación de contraseñas
# =============================================================================
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


# =============================================================================
# Internacionalización
# =============================================================================
LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_TZ = True


# =============================================================================
# Archivos estáticos
# =============================================================================
STATIC_URL = 'static/'


# =============================================================================
# Django REST Framework
# =============================================================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # Por seguridad, todos los endpoints requieren autenticación salvo que
    # la vista indique lo contrario (por ejemplo, el login con JWT).
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}


# =============================================================================
# Configuración de JWT
# =============================================================================
# El tiempo de vida del token de acceso se puede cambiar sin tocar el código:
#   set ACCESS_TOKEN_LIFETIME_MINUTES=15
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(
        minutes=int(os.environ.get('ACCESS_TOKEN_LIFETIME_MINUTES', 60))
    ),
    'REFRESH_TOKEN_LIFETIME': timedelta(
        days=int(os.environ.get('REFRESH_TOKEN_LIFETIME_DAYS', 1))
    ),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'AUTH_HEADER_TYPES': ('Bearer',),
}


# =============================================================================
# Swagger / drf-yasg
# =============================================================================
SWAGGER_SETTINGS = {
    # No se usa la sesión de Django; la autenticación es con JWT.
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': (
                'Token JWT de acceso. En Swagger escribe: '
                'Bearer <access_token>'
            ),
        },
    },
    'SECURITY_REQUIREMENTS': [{'Bearer': []}],
    'DOC_EXPANSION': 'none',
    'DEEP_LINKING': True,
    'SHOW_REQUEST_HEADERS': True,
    'PERSIST_AUTH': True,
}
