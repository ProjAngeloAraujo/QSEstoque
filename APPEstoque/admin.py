from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('email_usuario', 'nome_usuario', 'nome_completo', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email_usuario', 'nome_usuario', 'nome_completo')
    ordering = ('email_usuario',)
    fieldsets = (
        (None, {'fields': ('email_usuario', 'nome_usuario', 'nome_completo', 'password')}),
        ('Permissões', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email_usuario', 'nome_usuario', 'nome_completo', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

admin.site.register(Usuario, UsuarioAdmin)