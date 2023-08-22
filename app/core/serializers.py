from rest_framework import serializers
from .models import *


class FullNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullName
        fields = '__all__'


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ('id', 'title', 'description', 'completed', 'maintask')


class MainTaskSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source='fullname.full_name')
    
    class Meta:
        model = MainTask
        fields = ('id', 'user', 'title', 'fullname', 'completed')
    
