from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models.helper.enums.base_textchoice import BaseTextChoices


class Order_Status_Choices(BaseTextChoices):
    """
    Order_Status_Choices model represents various Order statuses.

    Attributes:
        APPROVED (str, str)
        REJECTED (str, str)
        PENDING (str, str)

    Relations:
        None
    """

    # APPROVED = 'approved'
    # REJECTED = 'rejected'
    # PENDING = 'pending'
    #
    # ORDER_STATUS_CHOICES = [
    #     (APPROVED , _("Approved")) ,
    #     (REJECTED , _("Rejected")) ,
    #     (PENDING , _("Pending")) ,
    # ]

    APPROVED = 'approved', _("Approved")
    REJECTED = 'rejected', _("Rejected")
    PENDING = 'pending', _("Pending")