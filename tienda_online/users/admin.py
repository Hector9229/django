from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin del usuario personalizado (email + teléfono)."""

    model = User
    ordering = ('email',)
    list_display = (
        'email',
        'first_name',
        'last_name',
        'phone',
        'is_active',
        'is_staff',
    )
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'groups')
    search_fields = ('email', 'first_name', 'last_name', 'phone')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            'Datos personales',
            {'fields': ('first_name', 'last_name', 'phone')},
        ),
        (
            'Permisos',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'first_name',
                    'last_name',
                    'phone',
                    'password1',
                    'password2',
                ),
            },
        ),
    )
