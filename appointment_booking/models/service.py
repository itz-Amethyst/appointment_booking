from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from typing import  Union

from appointment_booking.models import Company
from appointment_booking.models.helper.enums import Presentation_Choices


class Service(models.Model):
    """
    The `Service` model represents a service offering with various attributes and relationships.

    Attributes:
        title (CharField): The title of the service.
        company_id (ForeignKey): Company-Id associated with this service.
        description (TextField): A detailed description of the service.
        is_active (BooleanField): Indicates whether the service is active.
        can_accept_user_custom_time (BooleanField): Indicates if the service allows custom user scheduling.
        has_quantity (BooleanField): Indicates whether the service involves a quantity.
        price (DecimalField): The price of the service, specified with two decimal places.
        presentation (CharField): Represents the mode of the service (e.g., in-person, online, or hybrid).
        assigned_staffs (ForeignKey): A reference to a user (staff) assigned to the service. It can be null.
        sub_service (ForeignKey): Self-referencing relation to indicate a sub-service. It can also be null.
    """

    title: models.CharField = models.CharField(
        max_length = 255 ,
        unique = True ,
        verbose_name = _("Title") ,
        help_text = _("Title of the service") ,
        db_column = "title" ,
        error_messages = {
            'required': _("Title is required.") ,
            'unique': _("A service with this title already exists.") ,
        }
    )

    company_id: models.ForeignKey[Company] = models.ForeignKey(
        Company ,
        on_delete = models.CASCADE ,
        related_name = "company_id" ,
        verbose_name = _("Company-Id") ,
        help_text = _("Company-Id associated with this service") ,
        db_column = "company_id" ,
    )

    description: models.TextField = models.TextField(
        verbose_name = _("Description") ,
        help_text = _("Description of the service") ,
        db_column = "description" ,
        blank = True ,
        null = True
    )

    is_active: models.BooleanField = models.BooleanField(
        default = True ,
        verbose_name = _("Is Active") ,
        help_text = _("Indicates whether the service is active") ,
        db_column = "is_active"
    )

    can_accept_user_custom_time: models.BooleanField = models.BooleanField(
        default = False ,
        verbose_name = _("Can Accept User Custom Time") ,
        help_text = _("Can the service accept custom user times?") ,
        db_column = "can_accept_user_custom_time"
    )

    has_quantity: models.BooleanField = models.BooleanField(
        default = False ,
        verbose_name = _("Has Quantity") ,
        help_text = _("Does the service involve a quantity?") ,
        db_column = "has_quantity"
    )

    price: models.DecimalField = models.DecimalField(
        max_digits = 10 ,
        decimal_places = 2 ,
        verbose_name = _("Price") ,
        help_text = _("Price of the service") ,
        db_column = "price" ,
    )

    presentation: models.CharField = models.CharField(
        max_length = 20 ,
        choices = Presentation_Choices ,
        # Todo: Doubt?!
        default = Presentation_Choices.IN_PERSON.value,
        verbose_name = _("Presentation") ,
        help_text = _("Presentation mode of the service") ,
        db_column = "presentation"
    )

    # Relationships
    assigned_staffs: models.ManyToManyField = models.ForeignKey(
        settings.AUTH_USER_MODEL ,
        on_delete = models.SET_NULL ,
        related_name = "assigned_services" ,
        verbose_name = _("Assigned Staffs") ,
        help_text = _("Assigned staff for the service") ,
        blank = True
    )

    sub_service: models.ForeignKey[Union['Service' , None]] = models.ForeignKey(
        'self' ,
        on_delete = models.CASCADE ,
        related_name = "sub_services" ,
        verbose_name = _("Sub-Service") ,
        help_text = _("Sub-service associated with this service") ,
        db_column = "sub_service" ,
        null = True ,
        blank = True
    )

    class Meta:
        db_table = "services"
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        ordering = ["-is_active" , "title"]

        constraints = [
            models.CheckConstraint(
                check = models.Q(price__gte = 0) ,
                name = "non_negative_price" ,
                violation_error_message = _("Price must be non-negative.")
            ) ,
            models.CheckConstraint(
                check = models.Q(sub_service__isnull = True) | models.Q(sub_service__pk__ne = models.F('pk')) ,
                name = "no_self-reference_sub_service" ,
                violation_error_message = _("Sub-service cannot reference itself.") ,
            ) ,
        ]

    def clean( self ) -> None:
        """
        Custom validation logic to ensure data integrity.
        """
        if self.price < 0:
            raise ValidationError({
                "price": _("Price cannot be negative.")
            })

        if self.sub_service and self.sub_service == self:
            raise ValidationError({
                "sub_service": _("Sub-service cannot be itself.")
            })

        #? To apply only 1 layer relation limit
        # if self.sub_service:
        #     # Check if the sub-service has its own sub-service, preventing multiple layers
        #     if self.sub_service.sub_service:
        #         raise ValidationError({
        #             "sub_service": _(
        #                 "A service can only have one level of sub-service. Nested sub-services are not allowed.")
        #         })

        super().clean()

    def save( self , *args: list , **kwargs: dict ) -> None:
        """
        Override the save method to ensure validation before saving.
        """
        self.clean()
        super().save(*args , **kwargs)

    def __str__( self ) -> str:
        """
        String representation of the `Service` model.
        """
        return self.title