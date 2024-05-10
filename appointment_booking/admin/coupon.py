from django.contrib import admin
from appointment_booking.models import Coupon
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'start_date', 'expire_date', 'discount_percentage')
