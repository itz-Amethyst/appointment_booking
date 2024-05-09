from typing import Dict , List

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from rest_framework_simplejwt.tokens import RefreshToken


# from rest_framework_simplejwt.tokens import RefreshToken




class User(AbstractUser):
    """
    User model representing a user in the system.

    Attributes:
        email (models.EmailField): Email field for the user.

    Relations:
        None
    """

    email: models.EmailField = models.EmailField(
        verbose_name=_("Email"),
        help_text=_("This is the email address of the user."),
        db_comment=_("This is the email address of the user."),
        unique=True,
        validators=[validate_email]
    )

    phone_number: models.CharField = models.CharField(
        verbose_name = _("Phone Number") ,
        help_text = _("User's phone number.") ,
        unique = True ,  # Ensure unique phone numbers
        blank = False ,  # Phone number must not be empty
        null = True,  # Initially allow null
        error_messages = {
            'unique': _("This phone number is already associated with another user.") ,
        }
    )

    country: models.CharField = models.CharField(
        verbose_name = _("Country") ,
        max_length = 40 ,
        help_text = _("User's country.") ,
        blank = True ,  # Country is optional
    )
    REQUIRED_FIELDS =  ['phone_number', 'email',]


    class Meta:
        db_table: str = "users"
        db_table_comment: str = "This table contains all users in the system."
        verbose_name: str = _("User")
        verbose_name_plural: str = _("Users")
        ordering = ["-date_joined"]

        constraints: list = [
            models.CheckConstraint(
                check=models.Q(date_joined__gte=models.ExpressionWrapper(models.Value("NOW()"),
                                                                         output_field=models.DateTimeField())),
                name="check_date_joined",
                violation_error_message=_("The date joined must be in the past or present.")
            ),
            models.CheckConstraint(
                check=models.Q(last_login__gte=models.ExpressionWrapper(models.Value("NOW()"),
                                                                        output_field=models.DateTimeField())),
                name="check_last_login",
                violation_error_message=_("The last login must be in the past or present.")
            ),
            models.CheckConstraint(
                check=models.Q(last_login__gte=models.F('date_joined')),
                name="last_login_after_date_joined",
                violation_error_message=_("The last login must be after the date joined.")
            ),
            models.CheckConstraint(
                check = models.Q(phone_number__isnull = False) ,
                name = "phone_number_null_check" ,
                violation_error_message = _("Phone number cannot be null.") ,
            ) ,
        ]

    def generate_token( self ):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh) ,
            'access': str(refresh.access_token)
        }

    def clean( self ) -> None:
        """
        Custom validation logic to ensure data integrity.
        """

        # Optional country validation
        if self.country and not self.country.isalpha():
            raise ValidationError({
                "country": _("Country must only contain alphabetic characters.") ,
            })

        if self.phone_number is None:
            raise ValidationError({
                "phone_number": _("Phone number must not be null or empty.") ,
            })

        super().clean()


    def save( self , *args: List , **kwargs: Dict ) -> None:
        """
            Override the save method to perform validation before saving.
        """
        self.clean()
        super().save(*args , **kwargs)
