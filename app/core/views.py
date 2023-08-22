from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from .models import MainTask
from .renderers import *
from django.http import HttpResponse, JsonResponse
from .decorators import *


# CRUD operaions

class ListMainTask(generics.ListAPIView):  # Read
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
    

class DetailSubTask(generics.RetrieveAPIView):  # Update
    serializer_class = SubTaskSerializer
    renderer_classes = (UniversalRenderer, )
    queryset = SubTask.objects.all()

    # def get_object(self):
        # if self.request.user.groups.exists():

        #     if is_inspector(self.request.user):
        #         return "access denied, only executors can view subtasks"
            
        #     if is_executor(self.request.user):
        #         maintask_id = self.kwargs['pk']
        #         subtask_id = self.kwargs['sub_pk'] 
        #         print(maintask_id, subtask_id)

        #         queryset = SubTask.objects.filter(maintask_id=maintask_id, id=subtask_id)
        #         print(queryset)
            
        # return queryset


# class CreateMainTask(generics.CreateAPIView):  # Create
#     queryset = MainTask.objects.all()
#     serializer_class = MainTaskSerializer


# class DeleteMainTask(generics.DestroyAPIView):  # Delete
#     queryset = MainTask.objects.all()
#     serializer_class = MainTaskSerializer