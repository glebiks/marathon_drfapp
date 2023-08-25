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

        request = renderer_context['request']

        i_user = request.user.id

        # добавляем к каждой главной задаче список подзадач при ответе
        # проходить не по всем задачам а по задачам которые тебе назначены, если ты инспектор то по всем

        if User.objects.get(id = i_user).groups.exists():

            if is_inspector(User.objects.get(id = i_user)):
                for i in MainTask.objects.all():

                    # кол-во задач и номер
                    i.phone = i.user.username
                    i.all_tasks_num = len(SubTask.objects.filter(maintask_id=i.id))
                    tmp = SubTask.objects.filter(maintask_id = i.id)
                    i.completed_tasks_num = len(tmp.filter(ready=True))
                    i.save()

                    subtasks_temp = serializers.serialize('json', SubTask.objects.filter(maintask_id=i.id))
                    step1 = json.loads(subtasks_temp)
                    step2 = json.dumps([{'id':i['pk'], 'title': i['fields']['title'], 
                                        'description': i['fields']['description'], 
                                        'ready': i['fields']['ready']} for i in step1], ensure_ascii=False)
                    
                    if i.id-1 < len(data):
                        data[i.id-1]['subtasks'] = json.loads(step2)


            # исполнитель видит только свои задачи 
            if is_executor(User.objects.get(id = i_user)):
                for specific_main_task in MainTask.objects.filter(user = i_user):

                    # кол-во задач и номер
                    specific_main_task.phone = specific_main_task.user.username
                    specific_main_task.all_tasks_num = len(SubTask.objects.filter(maintask_id=specific_main_task.id))
                    tmp = SubTask.objects.filter(maintask_id = specific_main_task.id)
                    specific_main_task.completed_tasks_num = len(tmp.filter(ready=True))
                    specific_main_task.save()

                    # конкретные задачи
                    subtasks_temp = serializers.serialize('json', SubTask.objects.filter(maintask_id=specific_main_task.id))
                    step1 = json.loads(subtasks_temp)
                    step2 = json.dumps([{'id':i['pk'], 
                                         'title': i['fields']['title'], 
                                         'description': i['fields']['description'], 
                                         'ready': i['fields']['ready']} for i in step1], ensure_ascii=False)
                    
                    if specific_main_task.id-1 < len(data):
                        data[specific_main_task.id-1]['subtasks'] = json.loads(step2)

        
        response = ''
        if 'ErrorDetail' in str(data):
            response = json.dumps({'success': False, 'error': data}, ensure_ascii=False)
        else:
            response = json.dumps({'success': True, 'data': data}, ensure_ascii=False)

        return response
    