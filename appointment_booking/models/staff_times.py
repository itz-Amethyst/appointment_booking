from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import JSONField
from django.conf import settings

from core.models.core import CoreModel


class Staff_Times(CoreModel):
    """
    The `Staff_Times` model represents a schedule for a staff with specified working hours.

    Attributes:
        user (ForeignKey): Reference to a staff member in the User model.
        working_hours (JSONField): JSON data for working hours, with start and end times for each day.
    """

    user: models.ForeignKey[settings.AUTH_USER_MODEL] = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="schedules",
        verbose_name=_("User"),
        help_text=_("The staff member this schedule belongs to."),
        db_column="user_id",
    )

    working_hours: JSONField = models.JSONField(
        verbose_name=_("Working Hours"),
        help_text=_("Working hours for each day of the week."),
        default=dict,  # Initializes with an empty dictionary
        db_column="working_hours"
    )

    class Meta:
        db_table = "Staff_Times"
        verbose_name = _("Staff_Times")
        verbose_name_plural = _("Staff_Times")

        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    user__is_staff=True
                ),
                name="user_is_staff",
                violation_error_message=_("User must be a staff member.")
            ),
            # models.CheckConstraint(
            #     check = models.Q(
            #         working_hours__has_keys = ['sunday' , 'monday' , 'tuesday' , 'wednesday', 'saturday']
            #     ) ,
            #     name = "working_hours_all_days" ,
            #     violation_error_message = _("Working hours must contain all days of the week.")
            # ) ,
        ]

    def clean(self) -> None:
        """
        Custom validation logic to ensure data integrity and proper structure of `working_hours`.
        """
        if not self.user.is_staff:
            raise ValidationError({
                "user": _("User must be a staff member.")
            })

        if not isinstance(self.working_hours, dict):
            raise ValidationError({
                "working_hours": _("Working hours must be a valid JSON object.")
            })

        if not self.working_hours:
            raise ValidationError({
                "working_hours": _("At least one day must be specified in `working_hours`.")
            })

        # required_days = ["sunday", "monday", "tuesday", "wednesday", "saturday"]
        required_keys = ["start", "end"]

        #! Ensure all days are in `working_hours` with the correct structure
        # for day in required_days:
        #     if day not in self.working_hours:
        #         raise ValidationError({
        #             "working_hours": _(f"`working_hours` must contain {day}.")
        #         })
        #
        #     if not all(key in self.working_hours[day] for key in required_keys):
        #         raise ValidationError({
        #             "working_hours": _(f"`working_hours` for {day} must contain `start` and `end` times.")
        #         })

        for day, hours in self.working_hours.items():
            if not all(key in hours for key in required_keys):
                raise ValidationError({
                    "working_hours": _(f"`working_hours` for {day} must contain `start` and `end` times.")
                })

        super().clean()

    def __str__(self) -> str:
        """
        String representation of the `UserSchedule` model.
        """
        return f"Schedules for {self.user.username}"
