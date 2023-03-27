from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Product


@admin.register(Product)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'price', 'active', 'datetime_modified', ]
