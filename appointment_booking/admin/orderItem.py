from django.contrib import admin
from appointment_booking.models import OrderItem
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = ('price', 'quantity', 'reservation_code')
    readonly_fields = ['booking_id', 'order_id']
