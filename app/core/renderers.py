from rest_framework import renderers
import json

from django.core import serializers
from .models import SubTask


class GlobalTasksRenderer(renderers.JSONRenderer):

    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):

        response = ''
        if 'ErrorDetail' in str(data):
            response = json.dumps({'success': False, 'error': data}, ensure_ascii=False)
        else:
            response = json.dumps({'success': True, 'data': data}, ensure_ascii=False)

        return response