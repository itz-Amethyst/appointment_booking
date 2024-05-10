from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from appointment_booking.models import Category


@receiver(m2m_changed, sender=Category.services.through)
def update_total_services_on_m2m_changed(sender, instance, action, **kwargs):
    """
    Signal handler to update `total_services` when the `services` ManyToManyField changes.
    """
    if action in ['post_add', 'post_remove', 'post_clear']:
        # Recount the total number of services and update
        instance.update_total_services()
        instance.save()
