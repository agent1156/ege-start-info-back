from django.urls import path
from .views import ContactRequestCreateView # Импортируйте вашу вьюху

urlpatterns = [
    # ... другие маршруты ...
    path('contact/', ContactRequestCreateView.as_view(), name='contact-request'),
]