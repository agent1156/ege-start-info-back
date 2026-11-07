from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import ContactRequest
from .serializers import ContactRequestSerializer

class ContactRequestCreateView(generics.CreateAPIView):
    """Прием заявок с формы обратной связи"""
    queryset = ContactRequest.objects.all()
    serializer_class = ContactRequestSerializer
    permission_classes = [AllowAny] # Разрешаем доступ без авторизации