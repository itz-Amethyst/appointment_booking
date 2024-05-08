from django.db import models
class BaseTextChoices(models.TextChoices):
    """
    Base class for TextChoices with additional functionality to return a formatted string of choices.
    """

    @classmethod
    def get_available_choices(cls) -> str:
        """
        Returns a formatted string of all available choices in this TextChoices class.

        Returns:
            str: A comma-separated string of choice display names.
        """
        # Construct a comma-separated string of choice display names
        available_choices = ', '.join([str(choice.label) for choice in cls])
        return available_choices