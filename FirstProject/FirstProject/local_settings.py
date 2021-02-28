SECRET_KEY = '-(g#imh1x3piyyd!gakp@#9w+caj8@#u&8*v53fiu&cfa@s9&u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
