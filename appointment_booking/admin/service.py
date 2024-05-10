from django.contrib import admin
from django.utils.html import format_html
from appointment_booking.models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_id', 'is_active', 'price', 'presentation', 'preview_image')
    list_filter = ('is_active', 'presentation')
    search_fields = ('title', 'description', 'company_id__name')

    def preview_image(self, obj):
        first_picture = obj.get_generic_pictures().first()  # Use custom method to get the first picture
        if first_picture and first_picture.picture_url:
            return format_html(
                f'<img src="{first_picture.picture_url.url}" style="max-width: 50px; max-height: 50px;" />'
            )
        return "-"

    preview_image.short_description = "Preview"