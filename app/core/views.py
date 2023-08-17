from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from .models import *


# CRUD operaions

class ListGlobalTask(generics.ListAPIView):  # Read
    queryset = GlobalTask.objects.all()
    serializer_class = GlobalTaskSerializer


class DetailGlobalTask(generics.RetrieveAPIView):  # Update
    queryset = GlobalTask.objects.all()
    serializer_class = GlobalTaskSerializer


class CreateGlobalTask(generics.CreateAPIView):  # Create
    queryset = GlobalTask.objects.all()
    serializer_class = GlobalTaskSerializer


class DeleteGlobalTask(generics.CreateAPIView):  # Delete
    queryset = GlobalTask.objects.all()
    serializer_class = GlobalTaskSerializer