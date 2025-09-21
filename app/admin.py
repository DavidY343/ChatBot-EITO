from django.contrib import admin
from .models import SimulatedUser, ChatMessage

class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("session_id", "role", "content", "created_at")
    list_filter = ("role", "created_at")
    search_fields = ("session_id", "content")

@admin.register(SimulatedUser)
class SimulatedUserAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_vegan_or_vegetarian', 'created_at']
    list_filter = ['is_vegan_or_vegetarian', 'created_at']

    search_fields = ['name']
    
    readonly_fields = ['created_at']
    
    list_editable = ['is_vegan_or_vegetarian']
    
    fieldsets = [
        ('Información Básica', {
            'fields': ['name', 'is_vegan_or_vegetarian']
        }),
        ('Preferencias', {
            'fields': ['favorites']
        }),
        ('Metadata', {
            'fields': ['created_at'],
            'classes': ['collapse']
        })
    ]