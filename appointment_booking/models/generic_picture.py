from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from appointment_booking.models.helper.managers.picture import GenericPictureManager
from appointment_booking.models.helper.uploader.file_uploader import get_upload_path

class Generic_Picture(models.Model):
    """
    The `Generic_Picture` model represents a picture that can be associated with any other model via generic relations.

    Attributes:
        picture_url (ImageField): The URL of the picture.
        content_type (ForeignKey): The content type that this picture is associated with.
        object_id (PositiveIntegerField): The ID of the associated object.
        content_object (GenericForeignKey): The generic relation to the associated object.
    """

    objects = GenericPictureManager()  # Custom manager (if needed)

    picture_url: models.ImageField = models.ImageField(
        upload_to=get_upload_path,
        verbose_name=_("Picture"),
        help_text=_("Upload an image."),
        blank=False,
        null=False,
    )

    content_type: models.ForeignKey[ContentType] = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_("Content Type"),
        help_text=_("The content type that this picture is associated with."),
    )

    object_id: models.PositiveIntegerField = models.PositiveIntegerField(
        verbose_name=_("Object ID"),
        help_text=_("The ID of the associated object."),
    )

    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = "generic_pictures"
        verbose_name = _("Generic Picture")
        verbose_name_plural = _("Generic Pictures")
        ordering = ["-id"]  # Optional ordering, e.g., by latest ID first

        constraints = [
            models.CheckConstraint(
                check=models.Q(picture_url__isnull=False),
                name="picture_url_not_null",
                violation_error_message=_("Picture URL must not be null."),
            ),
        ]

    def clean(self) -> None:
        """
        Custom validation logic to ensure data integrity.
        """
        if not self.picture_url:
            raise ValidationError({
                "picture_url": _("Picture URL must not be empty."),
            })

        if not self.content_type:
            raise ValidationError({
                "content_type": _("Content type must be specified."),
            })

        if not isinstance(self.object_id, int) or self.object_id < 1:
            raise ValidationError({
                "object_id": _("Object ID must be a positive integer."),
            })

        super().clean()

    def __str__(self) -> str:
        """
        String representation of the `Generic_Picture` model.
        """
        return f"Picture for {self.content_object} - {self.picture_url}"
