from rest_framework import renderers
import json

from django.core import serializers
from .models import SubTask


class GlobalTasksRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):

        step1 = serializers.serialize('json', SubTask.objects.all())
        step2 = json.loads(step1)
        step3 = json.dumps([{'title': i['fields']['title'], 
                            'description': i['fields']['description'], 
                            'completed': i['fields']['completed']} for i in step2])
        step4 = json.loads(step3)

        response = ''
        if 'ErrorDetail' in str(data):
            response = json.dumps({'success': False, 'error': data}, ensure_ascii=False)
        else:
            response = json.dumps({'success': True, 'data': data + step4}, ensure_ascii=False)

        return response