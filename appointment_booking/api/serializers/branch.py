from rest_framework import serializers

from appointment_booking.models.branch import Branch

class BranchSerializer(serializers.ModelSerializer):
    company_id = serializers.PrimaryKeyRelatedField(source = "company", read_only = True)
    class Meta:
        model = Branch
        fields = "__all__"

    def update( self , instance , validated_data ):
        validated_data.pop('company_id' , None)
        return super().update(instance , validated_data)

    def create( self , validated_data ):
        validated_data.pop('company_id' , None)
        return super().create(validated_data)

    #! Duplicate code since we check this logic through model validation

    # def validate( self , attrs ):
    #     """
    #     Custom validation logic to validate `working_hours` and `excluded_times`.
    #     """
    #     working_hours = attrs.get('working_hours')
    #     excluded_times = attrs.get('excluded_times')
    #
    #     if not working_hours or not isinstance(working_hours , dict):
    #         raise serializers.ValidationError("Working hours must be a valid JSON object.")
    #
    #     weekday_structure = ["start" , "end"]
    #
    #     # Ensure `weekdays` is defined and contains 'start' and 'end'
    #     if "weekdays" not in working_hours or not all(
    #             key in working_hours["weekdays"] for key in weekday_structure):
    #         raise serializers.ValidationError("`working_hours` must contain `weekdays` with `start` and `end` times.")