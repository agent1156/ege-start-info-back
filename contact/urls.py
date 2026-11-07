from django.urls import path
from .views import ContactRequestCreateView

urlpatterns = [
    # Путь будет пустым '', так как префикс мы зададим в главном urls.py
    path('', ContactRequestCreateView.as_view(), name='contact-request-create'),
]