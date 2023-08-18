from rest_framework import renderers
import json

from django.core import serializers
from .models import SubTask


class GlobalTasksRenderer(renderers.JSONRenderer):

    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):

        # all_subtasks = serializers.serialize('json', SubTask.objects.filter(id in Glo))
        # all_subtasks_dict = json.loads(all_subtasks)
        # all_subtasks_edit = json.dumps([{'title': i['fields']['title'], 
        #                     'description': i['fields']['description'], 
        #                     'completed': i['fields']['completed']} for i in all_subtasks_dict])
        # all_subtasks_json = json.loads(all_subtasks_edit)




        response = ''
        if 'ErrorDetail' in str(data):
            response = json.dumps({'success': False, 'error': data}, ensure_ascii=False)
        else:
            response = json.dumps({'success': True, 'data': data}, ensure_ascii=False)

        return response