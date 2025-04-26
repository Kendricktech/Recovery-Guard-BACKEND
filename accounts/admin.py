from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    list_display = ('email', 'first_name', 'last_name', 'username', 'is_staff', 
                    'is_active', 'is_agent', 'is_customer')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_agent', 'is_customer')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'username')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 
                                   'groups', 'user_permissions')}),
        ('Roles', {'fields': ('is_agent', 'is_customer')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name', 'username')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

# Register the admin class
admin.site.register(CustomUser, CustomUserAdmin)