from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models.helper.enums.base_textchoice import BaseTextChoices


class Presentation_Choices(BaseTextChoices):
    """
    Presentation_Choices model represents various Presentation choices.

    Attributes:
        IN_PERSON (str, str)
        ONLINE (str, str)
        HYBRID (str, str)

    Relations:
        None
    """

    # IN_PERSON = 'in_person'
    # ONLINE = 'online'
    # HYBRID = 'hybrid'

    # PRESENTATION_CHOICES = [
    #     (IN_PERSON , _("In-Person")) ,
    #     (ONLINE , _("Online")) ,
    #     (HYBRID , _("Hybrid")) ,
    # ]

    IN_PERSON = 'in_person', _("In-Person")
    ONLINE = 'online', _("Online")
    HYBRID = 'hybrid', _("Hybrid")
