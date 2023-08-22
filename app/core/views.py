from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework import generics
from .serializers import *
from .models import *
from .renderers import *
from django.http import HttpResponse, JsonResponse
from .decorators import *
from rest_framework.views import APIView
from rest_framework.response import Response


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

            subtask.completed = not subtask.completed
            subtask.save()

            serializer = SubTaskReadySerializer(subtask)
            return Response({'success': True, 'data': serializer.data})
        
        return Response({'success': False, 'data': {'pk':pk, 'sub_pk':kwargs['sub_pk']}})










# class DetailSubTask(generics.RetrieveAPIView):  # Update
#     serializer_class = SubTaskSerializer
#     renderer_classes = (UniversalRenderer, )
#     queryset = SubTask.objects.all()

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