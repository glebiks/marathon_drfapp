from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework import generics
from .models import MainTask, SubTask, Status
from .renderers import MainTasksRenderer, UniversalRenderer
from django.http import HttpResponse, JsonResponse
from .decorators import is_executor, is_inspector
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TokenCreateSerializer, MainTaskSerializer, SubTaskSerializer, SubTaskReadySerializer
from django.contrib.auth.models import Group, User


# custom djoser respone
from djoser.conf import settings
from djoser import utils
from rest_framework import generics, status, permissions


# custom token view
class CustomTokenCreateView(utils.ActionViewMixin, generics.GenericAPIView):
    """
    Use this endpoint to obtain user authentication token.
    """
    serializer_class = TokenCreateSerializer
    permission_classes = [permissions.AllowAny]

    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = settings.SERIALIZERS.token
        content = {
            'success': True,
            'data': {
                'token': token_serializer_class(token).data["auth_token"],
                'role': str(User.objects.get(username=self.request.data["username"]).groups.first()),
                # 'role': str(User.objects.get(username=self.request.POST['username']).groups.first()),
                'user_id': User.objects.get(username=self.request.data["username"]).pk,
            }
        }
        return Response(
            data=content,
            status=status.HTTP_200_OK,
        )
    

# global status view

class Ready(APIView):
    def get(self, request, **kwargs):
        maintasks = MainTask.objects.all()
        if maintasks.filter(ready=False).count() == 0:
            return Response({'success': True, 'data': {"ready": True}})
        else: 
            return Response({'success': True, 'data': {"ready": False}})


class ListMainTask(generics.ListAPIView): 
    serializer_class = MainTaskSerializer
    renderer_classes = (MainTasksRenderer, )
    queryset = MainTask.objects.all()
    
    # def get_queryset(self):
    #     queryset = None
    #     if self.request.user.groups.exists():
    #         if is_executor(self.request.user):
    #             queryset = MainTask.objects.filter(user=self.request.user)
    #         if is_inspector(self.request.user):
    #             queryset = MainTask.objects.all()
    #     return queryset
    

class SubtaskReady(APIView):

    def get(self, request, pk, **kwargs):
        # subtasks = get_list_or_404(SubTask, maintask=pk)
        try:
            subtask_temp = SubTask.objects.filter(maintask_id = pk)
            subtask = subtask_temp.get(pk=kwargs['sub_pk'])
            serializer = SubTaskSerializer(subtask)
            return Response({'success': True, 'data': serializer.data})
        except:
            return Response({"success": False, 
                            "message": f"Subtask with {kwargs['sub_pk']} id does not exist in this main task"})
        # return Response({'success': False, 'data': {'pk':pk, 'sub_pk':kwargs['sub_pk']}})

    def post(self, request, pk, **kwargs):
        # change subtask ready
        # subtasks = get_list_or_404(SubTask, maintask=pk)
        try:
            subtasks_temp = SubTask.objects.filter(maintask_id = pk)
            subtask = subtasks_temp.get(pk=kwargs['sub_pk'])
            subtask.ready = not subtask.ready
            subtask.save()
            # serializer = SubTaskReadySerializer(subtask)

            # изменение статуса глобальной задачи 
            cnt = 0
            rec = MainTask.objects.get(id=pk)


            for i in subtasks_temp:
                if i.ready == False:
                    cnt += 1
            if cnt == 0:
                rec.ready = True
                rec.save()
            elif cnt > 0 and rec.ready == True:
                rec.ready = False
                rec.save()
            
            # возвращаем главную задачу 
            from django.core import serializers
            import json
            from django.db.models import Q

            # кол-во задач и номер
            rec.all_tasks_num = len(SubTask.objects.filter(maintask_id=rec.id))
            rec.phone = rec.user.username
            rec.all_tasks_num = len(SubTask.objects.filter(maintask_id=rec.id))
            tmp = SubTask.objects.filter(maintask_id = rec.id)
            rec.completed_tasks_num = len(tmp.filter(ready=True))
            rec.save()

            # подготавливаем данные для поля subtasks
            subtasks_temp = serializers.serialize('json', SubTask.objects.filter(maintask_id=rec.pk))
            step1 = json.loads(subtasks_temp)
            step2 = json.dumps([{'id':i['pk'], 'title': i['fields']['title'], 
                                'description': i['fields']['description'], 
                                'ready': i['fields']['ready']} for i in step1], ensure_ascii=False)
            
            # подготавливаем данные основной задачи
            main_task_ser = MainTaskSerializer(rec)
            temp = json.dumps(main_task_ser.data, ensure_ascii=False)
            temp = json.loads(temp)
            temp['subtasks'] = json.loads(step2)

            return Response({'success': True, 'data': temp})
        # return Response({'success': True, 'data': serializer.data})
        # return Response({'success': False, 'data': {'pk':pk, 'sub_pk':kwargs['sub_pk']}})

        except:
            return Response({"success": False, 
                            "message": f"Subtask with {kwargs['sub_pk']} id does not exist in this main task"})