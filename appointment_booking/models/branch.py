from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import JSONField
from appointment_booking.models.company import Company
from core.models.core import CoreModel


class Branch(CoreModel):
    """
    The `Branch` model represents a specific location or branch with various attributes.

    Attributes:
        company_id (ForeignKey): Reference to the `Company` model.
        city (CharField): The city where the location is situated.
        location (TextField): The exact address or description of the location.
        excluded_times (JSONField): A JSON field for times when the location is closed or unavailable.
        working_hours (JSONField): A JSON field for the location's working hours.
        available_on_weekends (BooleanField): Indicates if the location is available on weekends.
    """

    company_id: models.ForeignKey[Company] = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name=_("Main Company"),
        help_text=_("The company this location belongs to."),
        related_name="locations"
    )

    city: models.CharField = models.CharField(
        max_length=100,
        verbose_name=_("City"),
        help_text=_("The city where the location is situated."),
        db_column="city"
    )

    location: models.TextField = models.TextField(
        verbose_name=_("Location"),
        help_text=_("The exact address or description of the location."),
        db_column="location"
    )

    excluded_times: JSONField = models.JSONField(
        verbose_name=_("Excluded Times"),
        help_text=_("Times when the location is closed or unavailable."),
        default=dict,
        db_column="excluded_times"
    )

    working_hours: JSONField = models.JSONField(
        verbose_name=_("Working Hours"),
        help_text=_("The working hours for the location."),
        default=dict,  # Initializes an empty JSON object
        db_column="working_hours"
    )

    available_on_weekends: models.BooleanField = models.BooleanField(
        default=False,
        verbose_name=_("Available on Weekends"),
        help_text=_("Is the location available on weekends?"),
        db_column="available_on_weekends"
    )

    class Meta:
        db_table = "locations"
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        ordering = ["city", "location"]

        constraints = [
            models.CheckConstraint(
            check = models.Q(
                working_hours__has_key = 'weekdays'
            ) & models.Q(
                working_hours__weekdays__has_key = 'start'
            ) & models.Q(
                working_hours__weekdays__has_key = 'end'
            ) ,
            name = "working_hours_weekdays_present" ,
            violation_error_message = _("Working hours must contain `weekdays` with `start` and `end`.")
            ) ,
            models.UniqueConstraint(
                fields = ["city" , "location"] ,
                name = "unique_city_location" ,
                violation_error_message = _("A location with this city and location already exists.")
            ) ,
            models.CheckConstraint(
                check = models.Q(available_on_weekends__in = [True , False]) ,
                name = "available_on_weekends_boolean" ,
                violation_error_message = _("Available on weekends must be a boolean value.")
            ) ,
        ]

    def clean(self) -> None:
        """
        Custom validation logic to ensure data integrity and check structure of `working_hours` and `excluded_times`.
        """
        if not self.city:
            raise ValidationError({
                "city": _("City must not be empty.")
            })

        # Validate `working_hours`
        if not isinstance(self.working_hours, dict):
            raise ValidationError({
                "working_hours": _("Working hours must be a valid JSON object.")
            })

        weekday_structure = ["start", "end"]

        # Ensure `weekdays` is defined and contains 'start' and 'end'
        if "weekdays" not in self.working_hours or not all(
                key in self.working_hours["weekdays"] for key in weekday_structure):
            raise ValidationError({
                "working_hours": _("`working_hours` must contain `weekdays` with `start` and `end` times.")
            })

        # Validate `excluded_times`
        if not isinstance(self.excluded_times, dict):
            raise ValidationError({
                "excluded_times": _("Excluded times must be a valid JSON object.")
            })

        # Check for `weekdays` in `excluded_times`
        if "weekdays" not in self.excluded_times or not all(
                key in self.excluded_times["weekdays"] for key in weekday_structure):
            raise ValidationError({
                "working_hours": _("`excluded_times` must contain `weekdays` with `start` and `end` times.")
            })

        # Optional check for weekends
        if "weekends" in self.working_hours and not all(
                key in self.working_hours["weekends"] for key in weekday_structure):
            raise ValidationError({
                "working_hours": _("If defined, `weekends` in `working_hours` must contain `start` and `end` times.")
            })

        super().clean()

    def __str__(self) -> str:
        """
        String representation of the `Location` model.
        """
        return f"{self.company_id.company_name} - {self.city}"
