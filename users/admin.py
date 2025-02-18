from django.contrib import admin
from .models import User
from datetime import datetime, timedelta, time


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff', 'is_active', 'date_joined']
    list_editable = ['is_active']
    list_per_page = 10
    list_filter = ['is_staff', 'is_active', 'date_joined']
    ordering = ['username']
    readonly_fields = ['password_mask', 'date_joined']
    search_fields = ['id', 'user', 'email']
    exclude = ['password']

    def password_mask(self, user):
        return user.password[:5] + '*****' + user.password[-5:]
