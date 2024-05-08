from django.contrib.auth import authenticate
from rest_framework import serializers
from djoser.constants import Messages
from djoser.conf import settings

from core.models import User


class LoginUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 168, write_only = True)
    # Fields return
    username = serializers.CharField(max_length = 255, read_only = True)
    email = serializers.EmailField(max_length = 255 , read_only = True)
    access_token = serializers.CharField(max_length = 255 , read_only = True)
    refresh_token = serializers.CharField(max_length = 255 , read_only = True)

    class Meta:
        model = User
        fields = ['password', 'access_token', 'email', 'refresh_token', 'username']

    default_error_messages = {
        "invalid_credentials": Messages.INVALID_CREDENTIALS_ERROR ,
        "inactive_account": Messages.INACTIVE_ACCOUNT_ERROR ,
    }

    def __init__( self , *args , **kwargs ):
        super().__init__(*args , **kwargs)
        self.user = None
        self.fields[settings.LOGIN_FIELD] = serializers.CharField()


    def validate(self, attrs):
        password = attrs.get("password")
        params = {settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD)}
        self.user = authenticate(
            request = self.context.get("request") , **params , password = password
        )
        if not self.user:
            self.user = User.objects.filter(**params).first()
            if not self.user:
                self.fail("invalid_credentials")
            if self.user and not self.user.check_password(password):
                self.fail("invalid_credentials")

        if not self.user.is_active:
            self.fail("inactive_account")

        if self.user and self.user.is_active:
            user_tokens = self.user.generate_token()

            return {
                'email': self.user.email ,
                'username': self.user.username ,
                'access_token': str(user_tokens.get("access")) ,
                'refresh_token': str(user_tokens.get("refresh"))
            }

        self.fail("invalid_credentials")
