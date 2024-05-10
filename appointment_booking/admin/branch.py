from django.contrib import admin
from appointment_booking.models import Branch
@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('company_id', 'city', 'location')
