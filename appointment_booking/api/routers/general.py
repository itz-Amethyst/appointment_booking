# from rest_framework_nested import routers
from rest_framework import routers
from appointment_booking.api.views.booking import BookingViewSet
from appointment_booking.api.views.branch import BranchViewSet
from appointment_booking.api.views.category import CategoryViewSet
from appointment_booking.api.views.company import CompanyViewSet

router = routers.DefaultRouter()


router.register("bookings", BookingViewSet, basename="bookings")
router.register("branches", BranchViewSet, basename="branches")
router.register("categories", CategoryViewSet, basename="categories")
router.register("companies", CompanyViewSet, basename="companies")


urlpatterns = router.urls