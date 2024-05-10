from django.contrib import admin , messages
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from appointment_booking.admin.generic_picture import GenericPictureInline
from appointment_booking.models import Company
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'total_books')
    readonly_fields = ['total_books', 'branch_count', 'staff_count']

    @admin.display(ordering = 'total_books')
    def total_books( self , booking ):
        from django.utils.http import urlencode
        url = (
                reverse('appointment_booking:admin:bookings_changelist')
                + '?'
                + urlencode({
            'booking__id': str(booking.id)
        }))
        return format_html('<a href="{}">{} Total Books</a>' , url , booking.total_books)

    # def get_queryset( self , request ):
    #     return super().get_queryset(request).annotate(
    #         total_books = Count('bookings')
    #     )