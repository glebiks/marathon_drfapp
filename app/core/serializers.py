from rest_framework import serializers
from .models import MainTask, SubTask, Status, User, FullName
import json


class FullNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullName
        fields = '__all__'


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ('id', 'title', 'description', 'ready', 'maintask')

class SubTaskReadySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ('ready',)


class MainTaskSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source='fullname.full_name')
    
    class Meta:
        model = MainTask
        fields = ('id', 'user', 'title', 'fullname', 'ready')
    

# new
from django.conf import settings
from django.contrib.auth import authenticate
from djoser import constants

from django.utils.translation import gettext_lazy as _

class TokenCreateSerializer(serializers.Serializer):
    password = serializers.CharField(
        required=False, style={'input_type': 'password'}
    )

    default_error_messages = {
        'invalid_credentials': constants.Messages.INVALID_CREDENTIALS_ERROR,
        'inactive_account': constants.Messages.INACTIVE_ACCOUNT_ERROR,
    }

    def __init__(self, *args, **kwargs):
        super(TokenCreateSerializer, self).__init__(*args, **kwargs)
        self.user = None
        self.fields[User.USERNAME_FIELD] = serializers.CharField(
            required=False
        )

    def validate(self, attrs):
        self.user = authenticate(
            username=attrs.get(User.USERNAME_FIELD),
            password=attrs.get('password')
        )

        self._validate_user_exists(self.user)
        self._validate_user_is_active(self.user)
        return attrs
    

    def _validate_user_exists(self, user):
        if not user:
            raise serializers.ValidationError({
                'success': False,
                'message': 'invalid_credentials'
            })
        

    def _validate_user_is_active(self, user):
        if not user.is_active:
            raise serializers.ValidationError({
                'success': False,
                'message': 'inactive_account'
            })
            


# custom handler exeption
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['success'] = False
        response.data['message'] = "invalid credentials"
        print(response.data)

    return response