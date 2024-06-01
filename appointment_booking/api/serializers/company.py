from rest_framework import serializers
from appointment_booking.models import Company

class CompanySerializer(serializers.ModelSerializer):
    """
    Serializer for the Company model.
    """

    class Meta:
        model = Company
        fields = ('id', 'company_name', 'branch_count', 'staff_count', 'total_books')
        # Todo later filter these fields to only be seen by staffs
        read_only_fields = ('branch_count', 'staff_count', 'total_books')


