from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from core.models.core import CoreModel
from core.models.helper.enums.section_choices import Section_Choices


class VerificationCode(CoreModel):
    """
    The `VerificationCode` model represents a token used for various verification purposes.

    Attributes:
        user (ForeignKey): The user associated with the verification code.
        token (CharField): The unique token used for verification.
        created_date (DateTimeField): The date and time when the code was created.
        is_active (BooleanField): Indicates if the token is active.
        section (CharField): The section or purpose for which the code is used.
    """

    user: models.ForeignKey[settings.AUTH_USER_MODEL] = models.ForeignKey(
        settings.AUTH_USER_MODEL ,
        on_delete = models.CASCADE ,
        related_name = "verification_codes" ,
        verbose_name = _("User") ,
        help_text = _("The user who owns this verification code.") ,
        db_column = "user_id" ,
    )

    token: models.CharField = models.CharField(
        max_length = 100 ,
        unique = True ,
        verbose_name = _("Token") ,
        help_text = _("The unique token for verification.") ,
        db_column = "token" ,
    )

    created_date: models.DateTimeField = models.DateTimeField(
        verbose_name = _("Created Date") ,
        auto_now_add = True ,
        help_text = _("The date and time when this code was created.") ,
        db_column = "created_date" ,
    )

    is_active: models.BooleanField = models.BooleanField(
        default = True ,
        verbose_name = _("Is Active") ,
        help_text = _("Indicates if this verification code is active.") ,
        db_column = "is_active" ,
    )

    section: models.CharField = models.CharField(
        _("Section") ,
        max_length = 20 ,
        choices = Section_Choices.SECTION_CHOICES ,
        default = Section_Choices.RESET_PASSWORD ,
        help_text = _("The section or purpose for this verification code.") ,
        db_column = "section" ,
    )

    class Meta:
        db_table = "verification_codes"
        verbose_name = _("Verification Code")
        verbose_name_plural = _("Verification Codes")
        ordering = ["-created_date"]

        constraints = [
            models.CheckConstraint(
                check = models.Q(payment_status__in = list(Section_Choices.values())) ,
                name = "valid_payment_status" ,
                violation_error_message = _("Payment status must be one of the following: {choices}.").format(
                    choices = Section_Choices.get_available_choices()) ,
            ) ,
            models.UniqueConstraint(
                fields=["user", "section"],
                name="unique_user_section",
                violation_error_message=_("A unique token already exists for this user and section."),
            ),
        ]

    def clean(self) -> None:
        """
        Custom validation logic to ensure data integrity.
        """

        if self.section not in dict(Section_Choices.choices):
            raise ValidationError(
                _(f'The status of the answer must be: {Section_Choices.get_available_choices()} .') ,
                code = 'invalid'
            )

        super().clean()

    def __str__(self) -> str:
        """
        String representation of the `VerificationCode` model.
        """
        return f"{self.user.username} - {self.section} - {self.token}"
