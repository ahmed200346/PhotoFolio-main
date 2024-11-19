from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Champs à afficher dans la liste des utilisateurs
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active')
    
    # Champs qui seront cliquables pour afficher les détails d'un utilisateur
    list_display_links = ('username', 'email')
    
    # Champs disponibles pour la recherche
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    # Champs éditables en ligne
    list_editable = ('is_active',)
    
    # Configuration des filtres pour le panneau de filtrage
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    
    # Organisation des champs dans le formulaire d'édition d'un utilisateur
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email' , 'is_artist')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    # Champs à afficher lors de la création d'un nouvel utilisateur
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_staff')
        }),
    )
    ordering = ('username',)  # Tri des utilisateurs par nom d'utilisateur
