from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import LoggedUser, CustomUser
from .forms import CustomUserChangeForm, CustomUserCreateForm

@admin.register(LoggedUser)
class LoggedUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'logged_at')

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreateForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('first_name', 'last_name', 'email', 'is_staff', 'is_superuser')

    # Sao os dados de cadastro do usuario na area administrativa que podem ser acrescentados
    fieldsets = (
        (None, {
            "fields": (
                'email', 'password'
            )
        }),
        ('Informações Pessoais', {
            "fields": (
                'first_name', 'last_name', 'perfil_image'
            )
        }),
        ('Permissões', {
            "fields":(
                'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
            )
        }),
        ('Datas Importantes', {
            "fields":(
                'last_login', 'date_joined'
            )
        }),
        
    )
    
