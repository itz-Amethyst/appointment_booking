from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from appointment_booking.models.company import Company
from appointment_booking.models.branch import Branch
from appointment_booking.models.booking import Booking
from appointment_booking.models.staff_times import Staff_Times

@receiver(post_save, sender=Company)
def handle_company_save(sender, instance, created, **kwargs):
    if created:
        instance.update_statistics()
    else:
        instance.update_statistics()

@receiver(post_save, sender=Branch)
@receiver(post_delete, sender=Branch)
@receiver(post_save, sender=Booking)
@receiver(post_delete, sender=Booking)
@receiver(post_save, sender=Staff_Times)
@receiver(post_delete, sender=Staff_Times)
def handle_related_model_change(sender, instance, **kwargs):
    if sender == Booking:
        company = instance.main_id
    else:
        company = instance.company_id
    company.update_statistics()
