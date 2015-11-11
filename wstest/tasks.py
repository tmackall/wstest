'''
module: tasks.py - used to execute celery tasks
'''
# standard imports
from __future__ import absolute_import
import logging
import os

# celery imports
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wstest.settings')

# django imports
from django.conf import settings


# declare celery object
APP = Celery('wstest')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
APP.config_from_object('django.conf:settings')
APP.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# Get an instance of a LOGGER
LOGGER = logging.getLogger(__name__)


@APP.task
def add(a, b):
    '''
    function: add - adds 2 numbers
    '''
    try:
        sum = int(a) + int(b)
    except:
        LOGGER.error('Exception when adding %s and %s' % (a, b))
        return -1
    return sum
