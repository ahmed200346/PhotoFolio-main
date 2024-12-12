from django.contrib import admin
from .models import *

@admin.register(Art)
class ArtAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner','is_public')
    list_filter = ('owner',)
    search_fields = ('title', 'tags', 'owner__username')  
    readonly_fields = ('created_at',)  
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'file', 'tags', 'owner' , 'price','category')
        }),
        ('Date Information', {
            'fields': ('created_at', ),
            'classes': ('collapse',),
        }),
    )

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('art_title', 'username', 'created_at')  # Affiche Art, User et Date
    search_fields = ('art__title', 'user__username')  # Recherche par titre d'art et utilisateur
    list_filter = ('created_at',)  # Filtrage par date

    def art_title(self, obj):
        """Affiche le titre de l'art lié au like."""
        return obj.art.title
    art_title.short_description = "Titre de l'Art"

    def username(self, obj):
        """Affiche le nom d'utilisateur ayant liké."""
        return obj.user.username
    username.short_description = "Nom d'utilisateur"
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('art_title', 'username', 'text_preview', 'created_at')  # Affiche Art, User, Texte et Date
    search_fields = ('art__title', 'user__username', 'text')  # Recherche par titre d'art, utilisateur et texte
    list_filter = ('created_at',)  # Filtrage par date *
    def art_title(self, obj):
        """Affiche le titre de l'art lié au commentaire."""
        return obj.art.title
    art_title.short_description = "Titre de l'Art"

    def username(self, obj):
        """Affiche le nom d'utilisateur ayant commenté."""
        return obj.user.username
    username.short_description = "Nom d'utilisateur"

    def text_preview(self, obj):
        """Affiche un aperçu du texte du commentaire."""
        return obj.text[:50] + ("..." if len(obj.text) > 50 else "")
    text_preview.short_description = "Aperçu du commentaire"   
