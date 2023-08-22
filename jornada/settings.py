"""
Django settings for Jornada project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/~

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
import sys
from datetime import datetime
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, "jornada", "apps"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "insecure-8#rlup6o=)u5%%t#sovn7hhl6rlp4-47^61acxy6n@ily3r8%j"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    
    "rest_framework",
    "django_filters",
    "fontawesomefree",
    "django_extensions",
    "simple_history",
    
    "core",
    "custom_auth",
    "django_component",
    "geoposition",
    "adolescentes",
    "servidores",
    "unidades",
    "dominios",
    "processos",
    "solicitacoes",
    "alteracoes_vinculo",
    "educacao",
    "riscos",
    "ocorrencias",
    "atendimento_psicossocial",
    "atividades",
    "rotina_modulo",
    "shared_components",
    "tjdft",
    "prontuario",
    "central",
    "nai",
    "uama",
    "logs",
    "livro",
    "rede_de_apoio",
    "pia",
    "visitas",
    "ligacoes",
    "tutorial",
    "usuario_empresa",
    "posicao",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # My Middleware
    "core.middleware.AuthoringMiddleware",
    "core.middleware.PermissaoDeUnidadeMiddleware",
    "core.middleware.PermissaoDeAdolescenteMiddleware",
    "logs.middleware.RequestLogMiddleware",
    # "django_plotly_dash.middleware.BaseMiddleware",
]

ROOT_URLCONF = "jornada.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "core.context_processors.url_kwargs_object_injection",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "builtins": [
                "django.templatetags.static",
                "django_component.templatetags",
                "core.templatetags.custom_tags",
            ],
        },
    },
]


WSGI_APPLICATION = "jornada.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",
        "PORT": 5432,
    },
    'test': {
        'ENGINE': 'django.db.backends.sqlite3',
    }   
}


if 'test' in sys.argv and 'keepdb' in sys.argv:
    DATABASES['default']['TEST']['NAME'] = '/dev/shm/jornada.test.db.sqlite3'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_L10N = True

# USE_TZ = True

# Chart and data
X_FRAME_OPTIONS = "SAMEORIGIN"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_ROOT = BASE_DIR / "uploads"

MEDIA_URL = "/media/"

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "core.exceptions.custom_exception_handler",
    # 'DEFAULT_AUTHENTICATION_CLASSES': [
    #     'rest_framework.authentication.TokenAuthentication',
    #     'rest_framework.authentication.SessionAuthentication',
    # ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FormParser",
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 50,
}

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = LOGIN_URL

AUTH_USER_MODEL = "custom_auth.CustomUser"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DATETIME_FORMAT = "%d-%m-%Y-%H-%M-%S"

GEOPOSITION_BACKEND = "leaflet"

# Disable prefixing relative URLs with request.path, handle as absolute file paths
WEASYPRINT_BASEURL = ""




from dynaconf import DjangoDynaconf  # noqa

settings = DjangoDynaconf(
    __name__,
    load_dotenv=False,
    envvar_prefix="JORNADA",
    env_switcher="JORNADA_ENV",
    settings_files=["settings.toml"],
)
