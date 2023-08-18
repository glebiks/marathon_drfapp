from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from .models import GlobalTask
from .models import SubTask as SubTaskModel
from .renderers import *


# CRUD operaions

# test
# class SubTask(generics.ListAPIView):
#     serializer_class = SubTaskSerializer

#     def get_queryset(self):
#         queryset = SubTaskModel.objects.all()
#         return queryset


class ListGlobalTask(generics.ListAPIView):  # Read
    queryset = GlobalTask.objects.all()
    serializer_class = GlobalTaskSerializer
    renderer_classes = (GlobalTasksRenderer, )


class DetailGlobalTask(generics.RetrieveAPIView):  # Update
    queryset = GlobalTask.objects.all()
    serializer_class = GlobalTaskSerializer


class CreateGlobalTask(generics.CreateAPIView):  # Create
    queryset = GlobalTask.objects.all()
    serializer_class = GlobalTaskSerializer


class DeleteGlobalTask(generics.CreateAPIView):  # Delete
    queryset = GlobalTask.objects.all()
    serializer_class = GlobalTaskSerializer