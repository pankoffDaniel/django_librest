from os import environ


DEBUG = False
ALLOWED_HOSTS = ["*"]
SECRET_KEY = environ["SECRET_KEY"]


# SMTP

EMAIL_HOST = environ["EMAIL_HOST"]
EMAIL_PORT = environ["EMAIL_PORT"]
EMAIL_HOST_USER = environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = environ["EMAIL_HOST_PASSWORD"]
EMAIL_USE_SSL = environ["EMAIL_USE_SSL"]
EMAIL_USE_TLS = environ["EMAIL_USE_TLS"]


# Database

POSTGRES_PASSWORD = environ['POSTGRES_PASSWORD']
POSTGRES_HOST = environ['POSTGRES_HOST']
POSTGRES_DB = environ['POSTGRES_DB']
POSTGRES_USER = environ['POSTGRES_USER']
POSTGRES_PORT = environ['POSTGRES_PORT']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': POSTGRES_DB,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': POSTGRES_HOST,
        'PORT': POSTGRES_PORT,
    }
}
