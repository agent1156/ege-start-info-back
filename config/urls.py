from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from tasks.views import TaskViewSet, TaskNumberViewSet

router = DefaultRouter()
router.register('tasks', TaskViewSet, basename='tasks')
router.register('task-numbers', TaskNumberViewSet, basename='task-numbers')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Ваши приложения
    path('api/contact/', include('contact.urls')),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)