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