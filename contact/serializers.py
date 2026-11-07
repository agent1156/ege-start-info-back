from rest_framework import serializers
from .models import ContactRequest

class ContactRequestSerializer(serializers.ModelSerializer):
    """
    Сериализатор для формы обратной связи.
    Превращает JSON из Nuxt в объект модели ContactRequest.
    """
    class Meta:
        model = ContactRequest
        fields = ['id', 'name', 'phone', 'email', 'message', 'created_at']
        # Эти поля заполняются автоматически, мы их не принимаем от пользователя
        read_only_fields = ['id', 'created_at']