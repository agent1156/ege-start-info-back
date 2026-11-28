from rest_framework import viewsets
from .models import (
    InfoTopic, 
    LessonDifficulty, 
    ExamType, 
    LessonTag, 
    SchoolClass, 
    LessonPlan
)
from .serializers import (
    InfoTopicSerializer, 
    LessonDifficultySerializer, 
    ExamTypeSerializer, 
    LessonTagSerializer, 
    SchoolClassSerializer, 
    LessonPlanSerializer
)

# ==========================================
# 1. API СПРАВОЧНИКОВ
# ==========================================

class InfoTopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InfoTopic.objects.filter(is_active=True)
    serializer_class = InfoTopicSerializer

class LessonDifficultyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LessonDifficulty.objects.filter(is_active=True)
    serializer_class = LessonDifficultySerializer

class ExamTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ExamType.objects.filter(is_active=True)
    serializer_class = ExamTypeSerializer

class LessonTagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LessonTag.objects.filter(is_active=True)
    serializer_class = LessonTagSerializer

class SchoolClassViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SchoolClass.objects.filter(is_active=True)
    serializer_class = SchoolClassSerializer


# ==========================================
# 2. API ПЛАНОВ УРОКОВ
# ==========================================

class LessonPlanViewSet(viewsets.ReadOnlyModelViewSet):
    # Оставляем только активные уроки. Используем prefetch_related для оптимизации БД.
    queryset = LessonPlan.objects.filter(is_active=True).prefetch_related('tags', 'school_classes')
    serializer_class = LessonPlanSerializer

    # Эта функция позволяет фильтровать данные в URL (например, ?topic=1)
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Фильтр по теме (?topic=slug_темы)
        topic_slug = self.request.query_params.get('topic', None)
        if topic_slug:
            queryset = queryset.filter(topic__slug=topic_slug)
            
        # Фильтр по классу (?school_class=slug_класса)
        school_class_slug = self.request.query_params.get('school_class', None)
        if school_class_slug:
            queryset = queryset.filter(school_classes__slug=school_class_slug)
            
        # Фильтр по сложности (?difficulty=slug)
        difficulty_slug = self.request.query_params.get('difficulty', None)
        if difficulty_slug:
            queryset = queryset.filter(difficulty__slug=difficulty_slug)

        return queryset