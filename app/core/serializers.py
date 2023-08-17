from rest_framework import serializers
from .models import *


class GlobalTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalTask
        fields = ('id', 'user', 'title', 'completed')


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model: SubTask
        fields = ('id', 'relate_to', 'title', 'description', 'completed')