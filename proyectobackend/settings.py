import os
from pathlib import Path
from dotenv import load_dotenv
# Construir rutas dentro del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
# Cargar variables de entorno desde el archivo .env
load_dotenv(BASE_DIR / '.env')

# Clave secreta desacoplada
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-tu-clave-secreta-aqui')

# Modo DEBUG desacoplado
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Hosts permitidos desacoplados
allowed_hosts_raw = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost')
ALLOWED_HOSTS = [h.strip() for h in allowed_hosts_raw.split(',') if h.strip()]

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'gestion_reservas',
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

ROOT_URLCONF = 'proyectobackend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # DIRS le indica a Django que busque la plantilla 404.html en la carpeta templates raíz
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'proyectobackend.wsgi.application'

# Conexión a Base de Datos desacoplada mediante variables de entorno
db_engine = os.getenv('DB_ENGINE', 'django.db.backends.sqlite3')
db_name = os.getenv('DB_NAME', 'db.sqlite3')
if 'sqlite' in db_engine and not os.path.isabs(str(db_name)):
    db_name = BASE_DIR / db_name

DATABASES = {
    'default': {
        'ENGINE': db_engine,
        'NAME': db_name,
        'USER': os.getenv('DB_USER', ''),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', ''),
    }
}

# Validadores de contraseña
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Configuración regional
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'