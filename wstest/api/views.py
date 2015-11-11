'''
module: views.py - top-level module that handles LAF-related http requests.
'''
# standard imports
import logging

# django, celery imports
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import autocomplete_light

#
# project imports
from wstest.tasks import add

autocomplete_light.autodiscover()

# task web-server imports

# Get an instance of a LOGGER
LOGGER = logging.getLogger(__name__)


@csrf_exempt
def request_add(request, **kwargs):
    '''
    function: request_add() - http add interface
    '''
    status_ret = {'status': 0, 'sum': 0}
    if request.method != 'POST':
        status_ret = {'status': 11}
        return JsonResponse(status_ret)
    if 'val1' not in request.POST or 'val2' not in request.POST:
        LOGGER.error('val1  and val2 are mandatory POST data')
        status_ret = {'status': 22}
        return JsonResponse(status_ret)

    val1 = request.POST['val1']
    val2 = request.POST['val2']
    print('POST info: %s' % request.POST)

    LOGGER.info('request_add')
    task = add.apply_async(args=[val1, val2])
    task.ready()
    try:
        sum = task.get()
    except:
        LOGGER.error('exeception in celery add() call')
        status_ret = {'status': 33}
        return JsonResponse(status_ret)

    status_ret['sum'] = sum

    return JsonResponse(status_ret)
