from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from .models import MainTask
from .renderers import *
from django.http import HttpResponse
from .decorators import *


# CRUD operaions

class ListMainTask(generics.ListAPIView):  # Read
    serializer_class = MainTaskSerializer
    renderer_classes = (GlobalTasksRenderer, )
    def get_queryset(self):
        group = None
        queryset = None

        if self.request.user.groups.exists():
            group = self.request.user.groups.all()[0]
            print(group)
            if is_executor(self.request.user):
                queryset = MainTask.objects.filter(user=self.request.user)
            if is_inspector(self.request.user):
                queryset = MainTask.objects.all()


        return queryset
    

class DetailSubTask(generics.RetrieveAPIView):  # Update
    queryset = MainTask.objects.all()
    serializer_class = SubTaskSerializer


class DetailMainTask(generics.RetrieveAPIView):  # Update
    queryset = MainTask.objects.all()
    serializer_class = MainTaskSerializer


class CreateMainTask(generics.CreateAPIView):  # Create
    queryset = MainTask.objects.all()
    serializer_class = MainTaskSerializer


class DeleteMainTask(generics.DestroyAPIView):  # Delete
    queryset = MainTask.objects.all()
    serializer_class = MainTaskSerializer