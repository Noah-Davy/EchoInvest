from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import UserRegistrationForm


class CustomUserAdmin(UserAdmin):
    add_form = UserRegistrationForm
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']


admin.site.register(CustomUser, CustomUserAdmin)