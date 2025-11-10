from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Session


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser', )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_id', 'created_at', 'expires_at')
    list_filter = ('created_at', 'expires_at')
    search_fields = ('user__email', 'session_id')
    readonly_fields = ('created_at',)
