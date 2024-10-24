
from django.contrib import admin
from .models import Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_private', 'created_at')  # Poți adăuga câmpurile relevante pentru vizualizare
    list_filter = ('is_private', 'user')  # Filtru pentru a sorta după utilizator și dacă sunt private
