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

class Messages:
    # INVALID_CREDENTIALS_ERROR = _(f"'success': {False}, 'error': 'Unable to log in with provided credentials.'")
    INVALID_CREDENTIALS_ERROR = _("Unable to log in with provided credentials.")
    INACTIVE_ACCOUNT_ERROR = _("User account is disabled.")
    INVALID_TOKEN_ERROR = _("Invalid token for given user.")
    INVALID_UID_ERROR = _("Invalid user id or user doesn't exist.")
    STALE_TOKEN_ERROR = _("Stale token for given user.")
    PASSWORD_MISMATCH_ERROR = _("The two password fields didn't match.")
    USERNAME_MISMATCH_ERROR = _("The two {0} fields didn't match.")
    INVALID_PASSWORD_ERROR = _("Invalid password.")
    EMAIL_NOT_FOUND = _("User with given email does not exist.")
    CANNOT_CREATE_USER_ERROR = _("Unable to create account.")


class TokenCreateSerializer(serializers.Serializer):
    password = serializers.CharField(
        required=False, style={'input_type': 'password'}
    )

    default_error_messages = {
        'invalid_credentials': Messages.INVALID_CREDENTIALS_ERROR,
        'inactive_account': Messages.INACTIVE_ACCOUNT_ERROR,
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
            # self.fail('invalid_credentials')
            raise serializers.ValidationError({
                'success': False,
                'message': 'invalid_credentials'
            })
        

    def _validate_user_is_active(self, user):
        if not user.is_active:
            self.fail('inactive_account')
            


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