from django.utils import timezone
from djoser import utils
from djoser.serializers import UidAndTokenSerializer as BaseActivationSerializer , PasswordSerializer , \
    PasswordRetypeSerializer , UsernameRetypeSerializer , UsernameSerializer
from rest_framework.exceptions import ValidationError

from core.models import User


class UIUDTokenSerializer(BaseActivationSerializer):

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        try:
            uid = utils.decode_uid(self.initial_data.get("uid", ""))
            self.user = User.objects.get(pk=uid)
            # Idea implemented really feels good
            new_password = self.initial_data.get("new_password" , None)
            if new_password and self.user.check_password(new_password):
                raise ValidationError({"password": "New password cannot be the same as current password"})
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            key_error = "invalid_uid"
            raise ValidationError(
                {"uid": [self.error_messages[key_error]]}, code=key_error
            )

        is_token_valid = self.context["view"].token_generator.check_token(
            self.user, self.initial_data.get("token", "")
        )

        if is_token_valid:
            self.handle_token_validation(validated_data['token'])
            return validated_data
        else:
            key_error = "invalid_token"
            raise ValidationError(
                {"token": [self.error_messages[key_error]]}, code=key_error
            )

    def handle_token_validation(self, token):
        # Check if the token has expired (created more than 5 minutes ago)
        verification_code = self.user.verificationcode_set.filter(token = token).first()
        token_created_time = verification_code.created_date
        current_time = timezone.now()

        time_difference = current_time - token_created_time

        if time_difference.total_seconds() > 300:  # 5 minutes = 300 seconds
            raise ValidationError({"token": ["Token has expired please resend it"]}, code="expired_token")

        elif not verification_code.is_active:
            raise ValidationError({"token": ["Token has been already used"]})
        verification_code.is_active = False
        verification_code.save()


class ActivationSerializer(UIUDTokenSerializer):
    pass

class PasswordResetConfirmSerializer(UIUDTokenSerializer, PasswordSerializer):
    pass

class PasswordResetConfirmRetypeSerializer(UIUDTokenSerializer, PasswordRetypeSerializer):
    pass

class UsernameResetConfirmSerializer(UIUDTokenSerializer, UsernameSerializer):
    pass

class UsernameResetConfirmRetypeSerializer(UIUDTokenSerializer, UsernameRetypeSerializer):
    pass