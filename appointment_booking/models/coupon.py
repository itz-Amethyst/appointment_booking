from typing import Optional

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from appointment_booking.models.service import Service
from core.models.core import CoreModel


class Coupon(CoreModel):
    """
    The `Coupon` model represents a discount coupon with various attributes and constraints.

    Attributes:
        start_date (DateField): The starting date of the coupon.
        expire_date (DateField): The expiration date of the coupon.
        code (CharField): The unique code for the coupon.
        discount_percentage (IntegerField): The discount percentage for the coupon.
        usable_count (IntegerField): The number of times the coupon can be used.
        defined_by (ForeignKey): Reference to the user who defined the coupon.
        service_id (ForeignKey): Reference to the `Service` model. Can be null.
    """

    start_date: models.DateField = models.DateField(
        verbose_name=_("Start Date"),
        help_text=_("The start date of the coupon."),
        db_column="start_date",
    )

    expire_date: models.DateField = models.DateField(
        verbose_name=_("Expire Date"),
        help_text=_("The expiration date of the coupon."),
        db_column="expire_date",
    )

    code: models.CharField = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Code"),
        help_text=_("The unique code for the coupon."),
        db_column="code",
        error_messages={
            'unique': _("A coupon with this code already exists."),
        }
    )

    discount_percentage: models.IntegerField = models.IntegerField(
        verbose_name=_("Discount Percentage"),
        help_text=_("The discount percentage for the coupon."),
        db_column="discount_percentage",
    )

    usable_count: models.IntegerField = models.IntegerField(
        verbose_name=_("Usable Count"),
        help_text=_("The number of times the coupon can be used."),
        db_column="Usable_count",
    )

    defined_by: models.ForeignKey[settings.AUTH_USER_MODEL] = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="defined_coupons",
        verbose_name=_("Defined By"),
        help_text=_("The user who defined the coupon."),
        db_column="defined_by",
    )

    service_id: models.ForeignKey[Optional[Service]] = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        related_name="coupons",
        verbose_name=_("Service"),
        help_text=_("The service associated with the coupon."),
        db_column="service_id",
        null=True,
        blank=True
    )

    class Meta:
        db_table = "coupons"
        verbose_name = _("Coupon")
        verbose_name_plural = _("Coupons")

        constraints = [
            models.CheckConstraint(
                check=models.Q(start_date__lt=models.F("expire_date")),
                name="start_date_before_expire_date",
                violation_error_message=_("Start date must be before expire date."),
            ),
            models.CheckConstraint(
                check=models.Q(discount_percentage__gte=0) & models.Q(discount_percentage__lte=100),
                name="valid_discount_percentage",
                violation_error_message=_("Discount percentage must be between 0 and 100."),
            ),
            models.CheckConstraint(
                check=models.Q(Usable_count__gte=0),
                name="Usable_count_non_negative",
                violation_error_message=_("Usable count must be non-negative."),
            ),
        ]

    def clean(self) -> None:
        """
        Custom validation logic to ensure data integrity.
        """
        if self.start_date >= self.expire_date:
            raise ValidationError({
                "start_date": _("Start date must be before expire date."),
            })

        if self.discount_percentage < 0 or self.discount_percentage > 100:
            raise ValidationError({
                "discount_percentage": _("Discount percentage must be between 0 and 100."),
            })

        if self.usable_count < 0:
            raise ValidationError({
                "usable_count": _("Usable count must be non-negative."),
            })

        super().clean()

    def __str__(self) -> str:
        """
        String representation of the `Coupon` model.
        """
        return f"Coupon {self.code} - {self.discount_percentage}% off"
