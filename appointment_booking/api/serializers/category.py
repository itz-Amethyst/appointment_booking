from rest_framework import serializers
from appointment_booking.models.category import Category

class CategorySerializer(serializers.ModelSerializer):
    total_services = serializers.IntegerField(read_only = True)
    class Meta:
        model = Category
        fields = "__all__"

    def update( self , instance , validated_data ):
        validated_data.pop('total_services' , None)
        return super().update(instance , validated_data)

    def create( self , validated_data ):
        validated_data.pop('total_services' , None)
        return super().create(validated_data)