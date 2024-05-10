from django.contrib import admin
from appointment_booking.models import Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'total_services')
    readonly_fields = ['total_services']
