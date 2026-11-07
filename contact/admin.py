from django.contrib import admin
from .models import ContactRequest

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at')
    search_fields = ('name', 'phone', 'email', 'message')
    list_editable = ('is_processed',) # Позволяет отмечать галочкой прямо в списке
    readonly_fields = ('created_at',)