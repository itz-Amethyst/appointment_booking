from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from appointment_booking.models.helper.enums.order_status_choices import Order_Status_Choices
from core.models.core import CoreModel

available_choices = ', '.join([str(choice[1]) for choice in Order_Status_Choices.choices])

class Order(CoreModel):
    """
    The `Order` model represents an order with attributes related to the user, payment status, and other details.

    Attributes:
        user_id (ForeignKey): Reference to the user who made the order.
        is_multiple_booking (BooleanField): Indicates if this is a multiple booking.
        is_coupon_used (BooleanField): Indicates if a coupon was used.
        payment_status (CharField): Status of the payment.
        final_price (BigIntegerField): The final price for the order.
    """

    user_id: models.ForeignKey[settings.AUTH_USER_MODEL] = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name=_("User"),
        db_column="user_id",
    )

    is_multiple_booking: models.BooleanField = models.BooleanField(
        default=False,
        verbose_name=_("Is Multiple Booking"),
        help_text=_("Indicates if this is a multiple booking."),
        db_column="is_multiple_booking",
    )

    is_coupon_used: models.BooleanField = models.BooleanField(
        default=False,
        verbose_name=_("Is Coupon Used"),
        help_text=_("Indicates if a coupon was used."),
        db_column="is_coupon_used",
    )

    payment_status: models.CharField = models.CharField(
        max_length=10,
        choices=Order_Status_Choices.ORDER_STATUS_CHOICES,
        default=Order_Status_Choices.PENDING,
        verbose_name=_("Payment Status"),
        help_text=_("Status of the payment."),
        db_column="payment_status",
    )

    final_price: models.BigIntegerField = models.BigIntegerField(
        verbose_name=_("Final Price"),
        help_text=_("The final price for the order."),
        db_column="final_price",
    )

    class Meta:
        db_table = "orders"
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

        constraints = [
            models.CheckConstraint(
                check = models.Q(payment_status__in = list(Order_Status_Choices.values())) ,
                name = "valid_payment_status" ,
                violation_error_message = _("Payment status must be one of the following: {choices}.").format(
                    choices = available_choices) ,
            ) ,
            models.CheckConstraint(
                check=models.Q(final_price__gte=0),
                name="final_price_non_negative",
                violation_error_message=_("Final price must be non-negative."),
            ),
        ]

    def clean(self) -> None:
        """
        Custom validation logic to ensure data integrity.
        """

        if self.final_price < 0:
            raise ValidationError({
                "final_price": _("Final price must be non-negative."),
            })

        if self.payment_status not in list(Order_Status_Choices.values()):
            raise ValidationError({
                "payment_status": _("Invalid payment status. Must be one of the predefined choices."),
            })

        if self.payment_status not in dict(Order_Status_Choices.choices):
            raise ValidationError(
                _(f'The status of the answer must be: {available_choices} .') ,
                code = 'invalid'
            )

        super().clean()

    def __str__(self) -> str:
        """
        String representation of the `Order` model.
        """
        return f"Order by {self.user_id} - {self.payment_status}"
