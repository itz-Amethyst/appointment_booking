from django.utils.translation import gettext_lazy as _

from core.models.helper.enums.base_textchoice import BaseTextChoices


class Section_Choices(BaseTextChoices):
    """
    Section_Choices model represents various code section.

    Attributes:
        RESET_PASSWORD (str, str)
        ACTIVATION (str, str)
        RESET_USERNAME (str, str)

    Relations:
        None
    """

    # RESET_PASSWORD = 'reset_password'
    # ACTIVATION = 'activation'
    # RESET_USERNAME = 'reset_username'
    #
    # SECTION_CHOICES = [
    #     (RESET_PASSWORD , _('Reset Password')) ,
    #     (ACTIVATION , _('Activation')) ,
    #     (RESET_USERNAME , _('Reset Username')) ,
    # ]

    RESET_PASSWORD = 'reset_password' , _('Reset Password')
    ACTIVATION = 'activation' , _('Activation')
    RESET_USERNAME = 'reset_username' , _('Reset Username')