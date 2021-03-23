from .base import *

try:
    environ.Env.read_env(BASE_DIR('.env'))
except FileNotFoundError:
    pass

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': env.db()
}
