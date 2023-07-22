from .base import *

from django.contrib.messages import constants as messages

SECRET_KEY = 'django-insecure-%qkq2xferk1*np4@l$#%cpqgj!!_o(b2t#%_bhk0d4&08p97y$'

DEBUG = True

ALLOWED_HOSTS = []


MESSAGE_TAGS = {
messages.DEBUG: 'alert-info',
messages.INFO: 'alert-info',
messages.SUCCESS: 'alert-success',
messages.WARNING: 'alert-warning',
messages.ERROR: 'alert-danger',
}

EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_HOST_USER = 'e8614bc4b353eb'
EMAIL_HOST_PASSWORD = '753ebdea19b2ab'
EMAIL_PORT = '2525'


