from rest_framework import serializers
from .models import *


class FullNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullName
        fields = '__all__'


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ('title', 'description', 'completed')


class MainTaskSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)
    fullname = serializers.CharField(source='fullname.full_name')
    
    class Meta:
        model = MainTask
        fields = ('id', 'user', 'title', 'fullname', 'completed', 'subtasks')
    

