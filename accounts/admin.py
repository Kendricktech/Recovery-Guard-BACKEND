from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

#@admin.register(CustomUser)
#class CustomUserAdmin(UserAdmin):
#    search_fields = ['email', 'first_name', 'last_name']  # or however your model is defined
    #list_display = ['email', 'is_agent', 'is_customer']
    #exclude =['date_joined',]

admin.site.register(CustomUser)
