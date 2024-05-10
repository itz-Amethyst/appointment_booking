from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from appointment_booking.models import Booking
from core.models import User


class CreateBookingSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a booking while also creating a new user.
    Includes additional fields for first name, last name, and phone number.
    """

    first_name = serializers.CharField(max_length = 30)
    last_name = serializers.CharField(max_length = 30)
    phone_number = serializers.CharField(max_length = 15)


    class Meta:
        model = Booking
        fields = (
            "start_time" ,
            "end_time" ,
            "service_id" ,
            "main_id" ,
            "branch_id" ,
            "first_name" ,
            "last_name" ,
            "phone_number" ,
        )

    def create( self , validated_data ):
        # Extract user-related data
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        phone_number = validated_data.pop("phone_number")

        # Create a new user based on this data
        username = f"{first_name.lower()}.{last_name.lower()}"  # Example username pattern

        # Check if the user already exists to avoid duplicate usernames
        if User.objects.filter(username = username).exists():
            raise ValidationError("A user with this username already exists.")

        new_user = User.objects.create(
            username = username ,
            first_name = first_name ,
            last_name = last_name ,
        )

        # Set the password to the phone number for simplicity
        new_user.set_password(phone_number)
        new_user.save()

        # Create the booking with the newly created user as `booked_by`
        booking = Booking(
            booked_by = new_user ,
            **validated_data  # Rest of the booking data
        )

        booking.save()

        return booking