from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'is_active', 'date_joined']
    list_filter = ['is_superuser', 'is_moderator',
                   'is_pro', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'bio')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_moderator', 'is_pro', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

    readonly_fields = ['date_joined', 'last_login']

    def role(self, obj):
        """Display user role as a colored badge"""
        if obj.is_superuser:
            return '🔴 Admin'
        if obj.is_moderator:
            return '🟡 Moderator'
        if obj.is_pro:
            return '🟢 Pro'
        return '⚪ User'
    role.short_description = 'Role'
