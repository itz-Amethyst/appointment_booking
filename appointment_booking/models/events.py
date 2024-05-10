from datetime import date
from datetime import datetime
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import ExpressionWrapper , DateField
from django.utils.translation import gettext_lazy as _
from appointment_booking.models.company import Company
from appointment_booking.models.branch import Branch
from django.utils import timezone

from core.models.core import CoreModel


class Events(CoreModel):
    """
    The `Event` model represents a specific event with attributes related to branches and companies.

    Attributes:
        branch_id (ForeignKey): Reference to a `Branch` model.
        main_id (ForeignKey): Reference to the `Company` model.
        reason (TextField): Description of the reason for the event.
        off_date (DateField): The specific date for the event.
    """

    branch_id: models.ForeignKey[Branch] = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        verbose_name=_("Branch"),
        related_name="events",
        help_text=_("The branch related to this event."),
        db_column="branch_id"
    )

    main_id: models.ForeignKey[Company] = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name=_("Company"),
        related_name="events",
        help_text=_("The company this event belongs to."),
        db_column="main_id"
    )

    reason: models.TextField = models.TextField(
        verbose_name=_("Reason"),
        help_text=_("The reason for the event."),
        db_column="reason",
        blank=False
    )

    off_date: models.DateField = models.DateField(
        verbose_name=_("Off Date"),
        help_text=_("The specific date for the event."),
        db_column="off_date"
    )

    class Meta:
        db_table = "events"
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        ordering = ["-off_date"]

        constraints = [
            models.CheckConstraint(
                check = models.Q(
                    off_date__gt=models.ExpressionWrapper(models.Value("NOW()"),
                        output_field = models.DateField()
                    )
                ),
                name = "off_date_greater_than_today",
                violation_error_message = _("Off date must be greater than today.")
            ),

        ]

    def clean(self) -> None:
        """
        Custom validation logic to ensure data integrity.
        """
        if not self.reason:
            raise ValidationError({
                "reason": _("Reason must not be empty.")
            })

        if isinstance(self.off_date , str):
            try:
                # Attempt to convert the string to a date
                datetime.strptime(self.off_date , "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError({
                    "off_date": _("Off date must be in YYYY-MM-DD format.")
                })
        elif not isinstance(self.off_date , date):
            raise ValidationError({
                "off_date": _("Off date must be a valid date.")
            })

        if self.off_date <= timezone.now().date():
            raise ValidationError({
                "off_date": _("Off date must be greater than today.")
            })
        super().clean()

    def __str__(self) -> str:
        """
        String representation of the `Event` model.
        """
        return f"{self.reason} on {self.off_date}"
