from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = '-(g#imh1x3piyyd!ga56423+caj8@#u&8*v53fiu&cfa@s9&u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'egp_sas_packager',  # 'portal', 'apiuniver.cskz.kz' 90.143.187.127
        'USER': 'postgres', # 'postgres'
        'PASSWORD': 'postgres', # 'yereldar'
        'HOST': 'localhost', # ''
        'PORT': '5432', #
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]