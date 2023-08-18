from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from .models import MainTask
from .models import SubTask as SubTaskModel
from .renderers import *


# CRUD operaions

class ListMainTask(generics.ListAPIView):  # Read
    queryset = MainTask.objects.all()
    serializer_class = MainTaskSerializer


class DetailMainTask(generics.RetrieveAPIView):  # Update
    queryset = MainTask.objects.all()
    serializer_class = MainTaskSerializer


class CreateMainTask(generics.CreateAPIView):  # Create
    queryset = MainTask.objects.all()
    serializer_class = MainTaskSerializer


class DeleteMainTask(generics.CreateAPIView):  # Delete
    queryset = MainTask.objects.all()
    serializer_class = MainTaskSerializer