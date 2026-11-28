from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

# Импортируем все нужные ViewSet-ы (включая новый FilterOptionsView)
from tasks.views import TaskViewSet, TaskNumberViewSet, FilterOptionsView

# Создаем роутер для API задач
router = DefaultRouter()
router.register('tasks', TaskViewSet, basename='tasks')
router.register('task-numbers', TaskNumberViewSet, basename='task-numbers')

# Список всех URL-адресов проекта
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API контактов
    path('api/contact/', include('contact.urls')),
    
    # API задач (генерируется роутером)
    path('api/', include(router.urls)),
    path('api/', include('LessonPlan.urls')), 
    # НОВЫЙ ПУТЬ ДЛЯ СПИСКА ФИЛЬТРОВ
    path('api/filters/', FilterOptionsView.as_view(), name='filter-options'),
]

# Раздача картинок в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)