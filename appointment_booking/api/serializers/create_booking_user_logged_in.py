from rest_framework import serializers
from appointment_booking.models import Booking, Service, Company, Branch

class BookingWithoutUserCredentialsSerializer(serializers.ModelSerializer):
    """
    Serializer for creating bookings without explicitly providing user credentials.
    `booked_by` is inferred from the request context.
    """
    service_id = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
    main_id = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    branch_id = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all())

    class Meta:
        model = Booking
        fields = (
            "start_time",
            "end_time",
            "service_id",
            "main_id",
            "branch_id",
        )

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user  # Infer the user from the request context
        validated_data["booked_by"] = user  # Set the user automatically
        return super().create(validated_data)  # Continue with the regular create process
