from django.http import HttpResponse
from django.core.serializers import serialize
import json

class HttpResponseMixin(object):
    """
    This mixin is used to send the data in http response
    """
    def render_to_http_response(data,status=200):
        return HttpResponse(data,content_type='application/json',status=status)


