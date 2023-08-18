from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from .models import MainTask, SubTask
from .renderers import *


# CRUD operaions

class ListMainTask(generics.ListAPIView):  # Read
    queryset = MainTask.objects.all()
    serializer_class = MainTaskSerializer
    renderer_classes = (GlobalTasksRenderer, )


class DetailMainTask(generics.RetrieveAPIView):  # Update
    queryset = MainTask.objects.all()
    serializer_class = MainTaskSerializer


class CreateMainTask(generics.CreateAPIView):  # Create
    queryset = MainTask.objects.all()
    serializer_class = MainTaskSerializer


class DeleteMainTask(generics.CreateAPIView):  # Delete
    queryset = MainTask.objects.all()
    serializer_class = MainTaskSerializer