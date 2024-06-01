from rest_framework_nested import routers
from appointment_booking.api.views.booking import BookingViewSet
from appointment_booking.api.views.branch import BranchViewSet
from appointment_booking.api.views.category import CategoryViewSet

router = routers.DefaultRouter()


router.register("bookings", BookingViewSet, basename="bookings")
router.register("branches", BranchViewSet, basename="branches")
router.register("categories", CategoryViewSet, basename="categories")


urlpatterns = router.urls