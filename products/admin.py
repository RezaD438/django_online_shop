from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Product, Comment


class CommentsInLine(admin.TabularInline):  # admon.StackInLine
    model = Comment
    fields = ['product', 'author', 'body', 'stars', ]
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'price', 'active', 'datetime_modified', ]
    inlines = [CommentsInLine, ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'author', 'active', 'body', 'stars', 'datetime_created', ]
