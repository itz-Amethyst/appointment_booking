from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html
from django.contrib.contenttypes.admin import GenericTabularInline
from appointment_booking.models import Generic_Picture

class GenericPictureInline(GenericTabularInline):
    model = Generic_Picture
    extra = 1
    #? TOd
    # autocomplete_fields = ['picture_url']
    readonly_fields = ['thumbnail']

    # Display thumbnail in admin
    def thumbnail(self, instance):
        if instance.picture_url:
            return format_html(f'<img src="{instance.picture_url.url}" class="thumbnail" style="max-width: 100px; max-height: 100px;" />')
        return "-"
    thumbnail.short_description = "Preview"
