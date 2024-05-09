from django.contrib import admin
from core.models.verification_code import VerificationCode
@admin.register(VerificationCode)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ["user", "token", "is_active", "section"]
    search_fields = ["user"]
    autocomplete_fields = ["user"]
    list_per_page = 10