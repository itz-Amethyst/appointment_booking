from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from appointment_booking.models.service import Service
from core.models.core import CoreModel


class Category(CoreModel):
    """
    The `Category` model represents a category with a title and a reference to multiple services.

    Attributes:
        title (CharField): The title of the category.
        total_services (IntegerField): The total number of services in this category.
        services (ManyToManyField): A many-to-many relationship with the `Service` model.
    """

    title: models.CharField = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Title"),
        help_text=_("The title of the category"),
        db_column="title",
        error_messages={
            'required': _("Title is required."),
            'unique': _("A category with this title already exists."),
        }
    )

    total_services: models.IntegerField = models.IntegerField(
        default=0,
        verbose_name=_("Total Services"),
        help_text=_("Total number of services in this category"),
        db_column="total_services"
    )

    services: models.ManyToManyField = models.ManyToManyField(
        Service,
        related_name="categories",
        verbose_name=_("Services"),
        help_text=_("Services belonging to this category"),
        db_column="service_id"
    )

    class Meta:
        db_table = "categories"
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["title"]

        constraints = [
            models.CheckConstraint(
                check=models.Q(total_services__gte=0),
                name="total_services_non_negative",
                violation_error_message=_("Total services must be non-negative.")
            ),
            models.UniqueConstraint(
                fields=["title"],
                name="unique_category_title",
                violation_error_message=_("A category with this title already exists.")
            ),
        ]

    def clean(self) -> None:
        """
        Custom validation logic to ensure data integrity.
        """
        if self.total_services < 0:
            raise ValidationError({
                "total_services": _("Total services cannot be negative.")
            })

        if not self.title:
            raise ValidationError({
                "title": _("Title is required.")
            })

        super().clean()

    def __str__(self) -> str:
        """
        String representation of the `Category` model.
        """
        return self.title
