from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework import generics
from .serializers import *
from .models import *
from .renderers import *
from django.http import HttpResponse, JsonResponse
from .decorators import *
from rest_framework.views import APIView
from rest_framework.response import Response


# custom djoser respone
from djoser.conf import settings
from djoser import signals, utils
from django.contrib.auth.tokens import default_token_generator
from rest_framework import generics, status, views, viewsets

class CustomTokenCreateView(utils.ActionViewMixin, generics.GenericAPIView):
    """Use this endpoint to obtain user authentication token."""

    serializer_class = settings.SERIALIZERS.token_create
    permission_classes = settings.PERMISSIONS.token_create

    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = settings.SERIALIZERS.token
        content = {
            'success': True,
            'data': {
                'Token': token_serializer_class(token).data["auth_token"]
            }
        }
        return Response(
            data=content
        )
    

    
# CRUD operaions


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
    
    def get_queryset(self):
        queryset = None
        if self.request.user.groups.exists():
            if is_executor(self.request.user):
                queryset = MainTask.objects.filter(user=self.request.user)
            if is_inspector(self.request.user):
                queryset = MainTask.objects.all()
        return queryset
    

class SubtaskReady(APIView):

    def get(self, request, pk, **kwargs):
        # Get subtask details by pk
        subtasks = get_list_or_404(SubTask, maintask=pk)
        if (kwargs['sub_pk']-1) < len(subtasks):
            subtask = subtasks[kwargs['sub_pk']-1]
            serializer = SubTaskSerializer(subtask)
            return Response({'success': True, 'data': serializer.data})
        return Response({'success': False, 'data': {'pk':pk, 'sub_pk':kwargs['sub_pk']}})
    
    def post(self, request, pk, **kwargs):
        # change subtask ready
        subtasks = get_list_or_404(SubTask, maintask=pk)

        if (kwargs['sub_pk']-1) < len(subtasks):
            subtask = subtasks[kwargs['sub_pk']-1]
            subtask.ready = not subtask.ready
            subtask.save()
            serializer = SubTaskReadySerializer(subtask)

            # изменение статуса глобальной задачи 
            cnt = 0
            rec = MainTask.objects.get(id=pk)
            for i in subtasks:
                if i.ready == False:
                    cnt += 1
            if cnt == 0:
                rec.ready = True
                rec.save()
            elif cnt > 0 and rec.ready == True:
                rec.ready = False
                rec.save()
            return Response({'success': True, 'data': serializer.data})
        return Response({'success': False, 'data': {'pk':pk, 'sub_pk':kwargs['sub_pk']}})


# class CreateMainTask(generics.CreateAPIView):  # Create
#     queryset = MainTask.objects.all()
#     serializer_class = MainTaskSerializer


# class DeleteMainTask(generics.DestroyAPIView):  # Delete
#     queryset = MainTask.objects.all()
#     serializer_class = MainTaskSerializer