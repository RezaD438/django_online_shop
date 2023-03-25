from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomChangeForm, CustomCreationForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomCreationForm
    form = CustomChangeForm
    model = CustomUser
    list_display = ['email', 'username', ]

# admin.site.register(CustomUser, CustomUserAdmin)
