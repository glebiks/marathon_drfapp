from rest_framework import renderers
import json

from django.core import serializers
from .models import *

class UniversalRenderer(renderers.JSONRenderer):

    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):

        response = ''
        if 'ErrorDetail' in str(data):
            response = json.dumps({'success': False, 'error': data}, ensure_ascii=False)
        else:
            response = json.dumps({'success': True, 'data': data}, ensure_ascii=False)

        return response
    

class MainTasksRenderer(renderers.JSONRenderer):

    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):

        # добавляем к каждой главной задаче список подзадач при ответе
        for i in MainTask.objects.all():
            subtasks_temp = serializers.serialize('json', SubTask.objects.filter(maintask_id=i.id))
            step1 = json.loads(subtasks_temp)
            step2 = json.dumps([{'id':i['pk'], 'title': i['fields']['title'], 
                                'description': i['fields']['description'], 
                                'ready': i['fields']['ready']} for i in step1], ensure_ascii=False)
            if i.id-1 < len(data):
                data[i.id-1]['phone'] = i.user.username
                data[i.id-1]['subtasks'] = json.loads(step2)
                
            
        
        response = ''
        if 'ErrorDetail' in str(data):
            response = json.dumps({'success': False, 'error': data}, ensure_ascii=False)
        else:
            response = json.dumps({'success': True, 'data': data}, ensure_ascii=False)

        return response
    