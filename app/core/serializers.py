from rest_framework import serializers
from .models import *


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ('title', 'description', 'completed')

class MainTaskSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = MainTask
        fields = ('id', 'user', 'title', 'completed', 'subtasks')
