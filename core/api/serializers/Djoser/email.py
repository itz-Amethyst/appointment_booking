from djoser import email
from djoser.conf import settings
from core.api.serializers.Djoser.helper.email_context import fill_context_data
from core.models.verification_code import VerificationCode



class ActivationEmail(email.ActivationEmail):
    def get_context_data(self):
        context = super().get_context_data()
        return fill_context_data(context = context, url = settings.ACTIVATION_URL.format(**context), section = VerificationCode.ACTIVATION)

class PasswordResetEmail(email.PasswordResetEmail):
    def get_context_data( self ):
        context = super().get_context_data()
        return fill_context_data(context = context, url = settings.PASSWORD_RESET_CONFIRM_URL.format(**context), section = VerificationCode.RESET_PASSWORD)


class UsernameResetEmail(email.UsernameResetEmail):
    def get_context_data(self):
        context = super().get_context_data()
        return fill_context_data(context = context, url = settings.USERNAME_RESET_CONFIRM_URL.format(**context), section = VerificationCode.RESET_USERNAME)
