from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from appointment_booking.models.order import Order
from appointment_booking.models.booking import Booking
import uuid


class OrderItem(models.Model):
    """
    The `OrderItem` model represents an item in an order with specified attributes and constraints.

    Attributes:
        booking_id (ForeignKey): Reference to a booking.
        order_id (ForeignKey): Reference to an order.
        price (DecimalField): The price of the item.
        quantity (IntegerField): The quantity of the item, default is 1.
        total_price (BigIntegerField): The total price for the item.
        total_price_with_discount (BigIntegerField): The total price with discount applied. Can be `null`.
        reservation_code (UUIDField): A unique 14-digit code or GUID/UUID.
    """

    booking_id: models.ForeignKey[Booking] = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="order_items",
        verbose_name=_("Booking"),
        db_column="booking_id",
    )

    order_id: models.ForeignKey[Order] = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Order"),
        db_column="order_id",
    )

    price: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Price"),
        db_column="price",
    )

    quantity: models.IntegerField = models.IntegerField(
        default=1,
        verbose_name=_("Quantity"),
        db_column="quantity",
    )

    #? In fact this should be decimal field , however for mucking payment zarinpal only accepts integer field
    total_price: models.BigIntegerField = models.BigIntegerField(
        verbose_name=_("Total Price"),
        db_column="total_price",
    )

    total_price_with_discount: models.BigIntegerField = models.BigIntegerField(
        verbose_name=_("Total Price with Discount"),
        db_column="total_price_with_discount",
        null=True,
    )

    reservation_code: models.UUIDField = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        verbose_name=_("Reservation Code"),
        db_column="reservation_code",
    )

    class Meta:
        db_table = "order_items"
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gte=1),
                name="quantity_non_negative",
                violation_error_message=_("Quantity must be at least 1."),
            ),
            models.CheckConstraint(
                check=models.Q(total_price__gte=0),
                name="total_price_non_negative",
                violation_error_message=_("Total price must be non-negative."),
            ),
            # models.CheckConstraint(
            #     check=models.Q(
            #         total_price_with_discount__isnull=True  # If null, it's valid
            #     ) | models.Q(total_price_with_discount__gte=0),
            #     name="total_price_with_discount_non_negative",
            #     violation_error_message=_("Total price with discount must be non-negative."),
            # ),
        ]

    def clean(self) -> None:
        """
        Custom validation logic to ensure data integrity.
        """
        if self.quantity < 1:
            raise ValidationError({
                "quantity": _("Quantity must be at least 1."),
            })

        expected_total_price = self.price * self.quantity
        if self.total_price != expected_total_price:
            raise ValidationError({
                "total_price": _("Total price must equal `price * quantity`."),
            })

        # if self.total_price_with_discount is not None and self.total_price_with_discount < 0:
        #     raise ValidationError({
        #         "total_price_with_discount": _("Total price with discount must be non-negative."),
        #     })

        super().clean()

    def __str__(self) -> str:
        """
        String representation of the `OrderItem` model.
        """
        return f"Order item for {self.booking_id} - {self.reservation_code}"
