from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from appointment_booking.models.branch import Branch
from appointment_booking.api.serializers import BranchSerializer
from appointment_booking.api.permissions import Access_Retrieve_Permission

class BranchViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [Access_Retrieve_Permission]
    http_method_names = ["get", "post", "put", "patch"]
