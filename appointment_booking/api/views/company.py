from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from appointment_booking.models.company import Company
from appointment_booking.api.serializers import CompanySerializer
from appointment_booking.api.permissions import Access_Retrieve_Permission

class CompanyViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [Access_Retrieve_Permission]
    http_method_names = ["get", "post", "put", "patch"]

    def get_serializer_context( self ):
        return {"request": self.request}
