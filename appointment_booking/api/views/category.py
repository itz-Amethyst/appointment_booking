from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from appointment_booking.models.category import Category
from appointment_booking.api.serializers import CategorySerializer
from appointment_booking.api.permissions import Access_Retrieve_Permission

class CategoryViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [Access_Retrieve_Permission]
    http_method_names = ["get", "post", "put", "patch"]

    def get_serializer_context( self ):
        return {"request": self.request}
