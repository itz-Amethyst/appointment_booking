from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from typing import List, Dict
from my_app.managers import CompanyManager  # Custom manager

from core.models.core import CoreModel


class Company(CoreModel):
    """
    The `Company` model represents a business entity with various attributes.

    Attributes:
        company_name (CharField): Name of the company.
        branch_count (IntegerField): Total number of branches for the company.
        staff_count (IntegerField): Total number of staff.
        total_books (IntegerField): Total books in the company.
    """

    company_name: models.CharField = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Company Name"),
        help_text=_("The name of the company"),
        db_column="company_name",
        error_messages={
            'required': _("Company name is required."),
            'unique': _("A company with this name already exists."),
        }
    )

    branch_count: models.IntegerField = models.IntegerField(
        verbose_name=_("Branch Count"),
        help_text=_("Total number of branches"),
        validators=[MinValueValidator(0)],
        db_column="branch_count"
    )

    staff_count: models.IntegerField = models.IntegerField(
        verbose_name=_("Staff Count"),
        help_text=_("Total number of staff"),
        validators=[MinValueValidator(0)],
        db_column="staff_count"
    )

    total_books: models.IntegerField = models.IntegerField(
        verbose_name=_("Total Books"),
        help_text=_("Total number of books"),
        validators=[MinValueValidator(0)],
        db_column="total_book"
    )

    objects = CompanyManager()  # Assuming a custom manager

    class Meta:
        db_table = "company"
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
        ordering = ["-created_at", "company_name"]

        constraints = [
            models.CheckConstraint(
                check=Q(branch_count__gte=0) & Q(staff_count__gte=0) & Q(total_book__gte=0),
                name="non_negative_values",
                violation_error_message=_("Branch count, staff count, and total book must be non-negative."),
            ),
        ]

    def clean(self) -> None:
        """
        Validate the Company instance.
        """
        if self.branch_count < 0:
            raise ValidationError({"branch_count": _("Branch count cannot be negative.")})

        if self.staff_count < 0:
            raise ValidationError({"staff_count": _("Staff count cannot be negative.")})

        if self.total_books < 0:
            raise ValidationError({"total_book": _("Total book count cannot be negative.")})

        super().clean()

    def save(self, *args: List, **kwargs: Dict) -> None:
        """
        Override the save method to validate before saving.
        """
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """
        Return the string representation of the Company.
        """
        return self.company_name
