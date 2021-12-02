from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import MyUser


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'dob', 'is_active', 'is_admin', 'is_staff')
    search_fields = ('email', 'username',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(MyUser, UserAdmin)
