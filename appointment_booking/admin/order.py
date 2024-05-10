from django.contrib import admin
from appointment_booking.models import Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('final_price',)
    readonly_fields = ['is_multiple_booking', 'user_id']
