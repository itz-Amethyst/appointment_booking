from rest_framework import serializers
from appointment_booking.models import Booking


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Booking` model.
    """

    class Meta:
        model = Booking
        fields = ['start_time', 'end_time', 'service_id', 'is_canceled', 'payment_status']
