import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY AND DEBUG ---

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-26w936$xdpc-v#_2@$@x+^0mgz!lpp-r^)2dr@959df5gv(4jl"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")
if DEBUG:
    ALLOWED_HOSTS = ["*"]


# --- APP DEFINITION ---

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',
    'rest_framework.authtoken',
    'api',
    'corsheaders',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise is removed as per user request
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = "filmhub.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # DIRS is empty as we rely on APP_DIRS
        "DIRS": [], 
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

WSGI_APPLICATION = "filmhub.wsgi.application"

# --- DATABASE CONFIGURATION ---

DB_HOST_RENDER = os.environ.get('DB_HOST')

if DB_HOST_RENDER:
    # Production Mode (Render or other hosting)
    DB_HOST = DB_HOST_RENDER
    DB_NAME_VAL = os.environ.get('DB_NAME')
    DB_USER_VAL = os.environ.get('DB_USER')
    DB_PASSWORD_VAL = os.environ.get('DB_PASSWORD')
else:
    # CI/Local Mode
    DB_HOST = os.environ.get('CI_DB_HOST', 'localhost') 
    DB_NAME_VAL = os.environ.get('CI_DB_NAME', 'test_db_ci')
    DB_USER_VAL = os.environ.get('CI_DB_USER', 'user_ci')
    DB_PASSWORD_VAL = os.environ.get('CI_DB_PASSWORD', 'password_ci')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': DB_HOST, 
        'NAME': DB_NAME_VAL,
        'USER': DB_USER_VAL, 
        'PASSWORD': DB_PASSWORD_VAL,
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Ensure DB_HOST is set in production
if os.environ.get('DEBUG', 'False') == 'False' and not os.environ.get('DB_HOST'):
    raise ValueError("DB_HOST environment variable is not set for production!")

# --- PASSWORD VALIDATION & I18N ---

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# --- STATIC FILES MANAGEMENT (CRITICAL FOR CONTAINER PATHS) ---

STATIC_URL = "/static/" 

# STATIC_ROOT must be an absolute path that matches the Dockerfile's COPY destination: /app/static
# BASE_DIR is /app/api/filmhub. BASE_DIR.parent.parent resolves to /app.
STATIC_ROOT = os.path.join(BASE_DIR.parent.parent, 'static') 

# If not using WhiteNoise, we use the default storage backend.
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage' 

# Media files (for user uploads, if used)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR.parent.parent, 'media') 


# --- MISCELLANEOUS ---

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',')

if DEBUG:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "https://filmhub-frontend-n6i3.onrender.com",
    ]
    CORS_ALLOW_ALL_ORIGINS = True