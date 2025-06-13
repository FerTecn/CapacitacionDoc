from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
 
 
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('last_name_paterno', 'last_name_materno', 'curp', 'rol')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('last_name_paterno', 'last_name_materno', 'curp', 'rol')}),
    )
    list_display = ('username', 'first_name', 'last_name_paterno', 'last_name_materno', 'curp', 'rol', 'email','is_active')
    search_fields = ('username', 'first_name', 'last_name_paterno', 'last_name_materno', 'curp', 'email', 'rol')
    list_filter = ('rol', 'is_active')
