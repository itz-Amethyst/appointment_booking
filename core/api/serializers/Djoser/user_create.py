import phonenumbers
from djoser.serializers import UserCreatePasswordRetypeSerializer
from rest_framework import serializers

from core.models import User


class UserCreateSerializer(UserCreatePasswordRetypeSerializer):
    phone_number = serializers.CharField(required = True)
    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        fields = ['id','first_name', 'last_name', 'username', 'email', 'password', 'phone_number',
            'gender', 'company_name']

    def validate_phone_number( self , value ):
        if not value:
            raise serializers.ValidationError("Phone number required") # If the phone number is not provided, don't perform further validation

        # Validate phone_number
        phone_number = str(value)
        # if user entered 0930... (this should be checked in front side)
        # if phone_number.startswith('0'):
        #     phone_number = '+98' + phone_number[1:]
        # else:
        #     phone_number = '+' + phone_number

        #! To clean strings from number
        # phone_number = ''.join(c for c in value if c.isdigit() or c == '+')

        if not value.startswith('+') or any(not c.isdigit() for c in value[1:]):
            raise serializers.ValidationError("Invalid characters in the phone number")

        if phone_number:
            try:

                parsed_number = phonenumbers.parse(phone_number, None)
                if not phonenumbers.is_valid_number(parsed_number):
                    raise serializers.ValidationError("Invalid phone number")
            except phonenumbers.NumberParseException:
                raise serializers.ValidationError("Invalid phone number format")

            if User.objects.filter(phone_number = phone_number).exists():
                raise serializers.ValidationError("Phone number already exists in the database")

        return phone_number
