from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_superuser", "phone_number", "country")
    search_fields = ("username", "first_name", "last_name", "phone_number")
    ordering = ("username",)
    fieldsets = (
        (None ,
         {"fields": ("username" , "email" , "password" , "first_name" , "last_name" , "phone_number")}) ,
        ("Permissions" , {"fields": ("is_staff" , "is_superuser" , "groups" , "user_permissions")}) ,
        ("Important dates" , {"fields": ("last_login" , "date_joined")}) ,
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2", "first_name", "last_name", "phone_number", "country"),
            },
        ),
    )
