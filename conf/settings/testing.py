from .base import *
import logging

os.environ['DATABASE_URL'] = os.environ['DATABASE_TEST_URL']

DATABASES = {
    'default': env.db()
}

# we don't want logging while running tests.
logging.disable(logging.CRITICAL)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

INTERNAL_IPS = (
    '127.0.0.1',
)

DEBUG = False
TEMPLATE_DEBUG = DEBUG
TESTS_IN_PROGRESS = True
