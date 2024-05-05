from django.core.validators import RegexValidator , MinLengthValidator

from django.db import models
from django.utils.translation import gettext_lazy as _



class Profile(models.Model):
    user: models.OneToOneField = models.OneToOneField(
        "core.User" ,
        on_delete = models.CASCADE ,
        related_name = "profile" ,
        verbose_name = _("User") ,
    )

    first_name: models.CharField = models.CharField(
        max_length = 50 ,
        validators = [MinLengthValidator(2)] ,
        verbose_name = _("First Name") ,
    )

    last_name: models.CharField = models.CharField(
        max_length = 50 ,
        validators = [MinLengthValidator(2)] ,
        verbose_name = _("Last Name") ,
    )

    phone_number: models.CharField = models.CharField(
        max_length = 15 ,
        validators = [RegexValidator(r"^\+?[0-9]*$" , _("Enter a valid phone number"))] ,
        verbose_name = _("Phone Number") ,
    )

    country_code: models.CharField = models.CharField(
        max_length = 3 ,
        validators = [RegexValidator(r"^[A-Z]{2,3}$" , _("Enter a valid country code"))] ,
        verbose_name = _("Country Code") ,
    )

    address: models.TextField = models.TextField(
        blank = True ,
        null = True ,
        verbose_name = _("Address") ,
    )

    # For assigned_staffs requires rethinking
    bio: models.TextField = models.TextField(
        max_length = 1000 ,
        blank = True ,
        null = True ,
        verbose_name = _("Bio") ,
    )

    class Meta:
        db_table = "profile"
        db_table_comment = _("This table contains user profiles.")
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        constraints = [
            models.CheckConstraint(
                check = models.Q(first_name__isnull = False) ,
                name = "check_first_name" ,
                violation_error_message = _("First name cannot be null.")
            ) ,
            models.CheckConstraint(
                check = models.Q(last_name__isnull = False) ,
                name = "check_last_name" ,
                violation_error_message = _("Last name cannot be null.")
            ) ,
            models.CheckConstraint(
                check = models.Q(phone_number__regex = r"^\+?[0-9]*$") ,
                name = "check_valid_phone_number" ,
                violation_error_message = _("Phone number must be valid.") ,
            ) ,
        ]


    def __str__( self ):
        return f"{self.user} >> {self.bio}"