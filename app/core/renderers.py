from rest_framework import renderers
import json

from django.core import serializers
from .models import *
from django.db.models import Q
from .decorators import is_inspector, is_executor

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
        # проходить не по всем задачам а по задачам которые тебе назначены, если ты инспектор то по всем
        if self.request.user.groups.exists():
            if is_inspector(self.request.user):
                for i in MainTask.objects.all():
                    subtasks_temp = serializers.serialize('json', SubTask.objects.filter(maintask_id=i.id))
                    step1 = json.loads(subtasks_temp)
                    step2 = json.dumps([{'id':i['pk'], 'title': i['fields']['title'], 
                                        'description': i['fields']['description'], 
                                        'ready': i['fields']['ready']} for i in step1], ensure_ascii=False)
                    if i.id-1 < len(data):
                        data[i.id-1]['phone'] = i.user.username
                        data[i.id-1]['completed_tasks_num'] = len(SubTask.objects.filter(Q(maintask_id=i.id) and Q(ready=True)))
                        data[i.id-1]['all_tasks_num'] = len(SubTask.objects.filter(maintask_id=i.id))
                        data[i.id-1]['subtasks'] = json.loads(step2)
            
            if is_executor(self.request.user):
                for i in MainTask.objects.filter(user = self.request.user):
                    subtasks_temp = serializers.serialize('json', SubTask.objects.filter(maintask_id=i.id))
                    step1 = json.loads(subtasks_temp)
                    step2 = json.dumps([{'id':i['pk'], 'title': i['fields']['title'], 
                                        'description': i['fields']['description'], 
                                        'ready': i['fields']['ready']} for i in step1], ensure_ascii=False)
                    if i.id-1 < len(data):
                        data[i.id-1]['phone'] = i.user.username
                        data[i.id-1]['completed_tasks_num'] = len(SubTask.objects.filter(Q(maintask_id=i.id) and Q(ready=True)))
                        data[i.id-1]['all_tasks_num'] = len(SubTask.objects.filter(maintask_id=i.id))
                        data[i.id-1]['subtasks'] = json.loads(step2)
        
        response = ''
        if 'ErrorDetail' in str(data):
            response = json.dumps({'success': False, 'error': data}, ensure_ascii=False)
        else:
            response = json.dumps({'success': True, 'data': data}, ensure_ascii=False)

        return response
    