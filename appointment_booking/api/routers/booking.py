from rest_framework_nested import routers
from appointment_booking.api.views.booking import BookingViewSet


router = routers.DefaultRouter()


router.register("bookings", BookingViewSet, basename="bookings")


urlpatterns = router.urls