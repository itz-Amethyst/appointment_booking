from django.db import models
from django.utils.translation import gettext_lazy as _


class Presentation_Choices(models.TextChoices):
    """
    Presentation_Choices model represents various Presentation choices.

    Attributes:
        IN_PERSON (str, str)
        ONLINE (str, str)
        HYBRID (str, str)

    Relations:
        None
    """

    IN_PERSON = 'in_person'
    ONLINE = 'online'
    HYBRID = 'hybrid'

    PRESENTATION_CHOICES = [
        (IN_PERSON , _("In-Person")) ,
        (ONLINE , _("Online")) ,
        (HYBRID , _("Hybrid")) ,
    ]
