from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ваш-ключ'

# SECURITY WARNING: don't run with debug turned on in production!
# ВАЖНО: Для локальной разработки здесь должно быть True
DEBUG = True

# ВАЖНО: Разрешаем локальные адреса
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Application definition
INSTALLED_APPS = [
    "jazzmin",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Сторонние приложения
    'rest_framework',
    'corsheaders',
    
    # Ваши приложения
    'api',
    'contact', 
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # <--- ДОБАВИТЬ САМЫМ ПЕРВЫМ
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# ЭТОГО БЛОКА У ВАС НЕ ХВАТАЛО
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
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =========================================
# ВАШИ НАСТРОЙКИ (CORS и DRF)
# =========================================

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

# =========================================
# НАСТРОЙКИ ДИЗАЙНА АДМИНКИ (JAZZMIN)
# =========================================
JAZZMIN_SETTINGS = {
    # Заголовки
    "site_title": "IT START Admin",
    "site_header": "IT START",
    "site_brand": "IT START", # Логотип или текст в левом верхнем углу
    "welcome_sign": "Добро пожаловать в панель управления",
    "copyright": "IT START © 2026",

    # Ссылки в верхнем меню
    "topmenu_links": [
        {"name": "На сайт", "url": "http://localhost:3000", "new_window": True},
    ],

    # Иконки для моделей (можно использовать FontAwesome)
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "contact.contactrequest": "fas fa-envelope", # Иконка для ваших заявок
    },

    # Кастомизация цветов (UI Tweaks)
    "ui_tweaks": {
        "navbar": "navbar-dark", # Темная шапка
        "no_navbar_border": True,
        "sidebar": "sidebar-dark-primary", # Темный сайдбар
        "sidebar_nav_child_indent": True,
        "sidebar_nav_compact_style": True,
        "sidebar_nav_legacy_style": False,
        "sidebar_nav_flat_style": False,
        "theme": "default", # Можно попробовать "darkly", "flatly" и т.д.
        "button_classes": {
            "primary": "btn-primary",
            "secondary": "btn-secondary",
            "info": "btn-info",
            "warning": "btn-warning",
            "danger": "btn-danger",
            "success": "btn-success"
        }
    }
}