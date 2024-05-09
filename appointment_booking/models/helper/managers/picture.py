from django.contrib.contenttypes.models import ContentType
from django.db import models

class GenericPictureManager(models.Manager):
    def get_pictures_for(self, obj_type, obj_id):
        # Delayed import to prevent circular imports
        from appointment_booking.models.generic_picture import Generic_Picture
        content_type = ContentType.objects.get_for_model(obj_type)

        return Generic_Picture.objects \
            .filter(
                content_type=content_type,
                object_id=obj_id
            )