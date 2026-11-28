from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    InfoTopicViewSet, 
    LessonDifficultyViewSet, 
    ExamTypeViewSet, 
    LessonTagViewSet, 
    SchoolClassViewSet, 
    LessonPlanViewSet
)

router = DefaultRouter()
# Справочники
router.register(r'topics', InfoTopicViewSet)
router.register(r'difficulties', LessonDifficultyViewSet)
router.register(r'exam-types', ExamTypeViewSet)
router.register(r'tags', LessonTagViewSet)
router.register(r'classes', SchoolClassViewSet) # <-- Для страницы "Классы"
# Основная сущность
router.register(r'lessons', LessonPlanViewSet)  # <-- Для страницы "Список планов" и "Детальная"

urlpatterns = [
    path('', include(router.urls)),
]