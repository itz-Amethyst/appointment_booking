from djoser.serializers import UserSerializer as BaseUserSerializer

from appointment_booking.api.serializers.booking import BookingSerializer


class UserSerializer(BaseUserSerializer):

    applied_booking = BookingSerializer(many = True, read_only = True)

    class Meta(BaseUserSerializer.Meta):
        fields = ['first_name', 'last_name', 'username', 'email', 'last_login', 'is_staff', 'date_joined', 'country', 'phone_number', 'company_name', 'applied_booking']
