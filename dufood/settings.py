# settings.py

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# 환경 변수에서 SECRET_KEY를 가져옵니다.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'default-secret-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False  # 배포 환경에서는 False로 설정

# ALLOWED_HOSTS는 Koyeb에서 제공하는 URL을 포함시킵니다.
ALLOWED_HOSTS = ['bare-willabella-dufood-1844b7ff.koyeb.app', 'localhost', '127.0.0.1']  # Koyeb의 URL로 수정

# Application definition
INSTALLED_APPS = [
    'restaurants.apps.RestaurantsConfig',  # 프로젝트 앱
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # SQLite 사용
        'NAME': BASE_DIR / 'db.sqlite3',         # db.sqlite3 파일을 최상위 폴더에서 찾도록 설정
    }
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dufood.urls'

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

WSGI_APPLICATION = 'dufood.wsgi.application'

# DATABASES 설정 (SQLite 사용)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # SQLite 사용
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),  # db.sqlite3 파일 경로
    }
}

# Password validation
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
LANGUAGE_CODE = 'ko'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# 로컬에서 정적 파일을 저장할 디렉토리
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles'),  # 프로젝트 내 정적 파일 디렉토리
]

# Koyeb에서 정적 파일을 저장할 최종 경로
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_root')

# Media files (이미지, 동영상 등)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 로그인 URL 설정
LOGIN_URL = '/login/'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
