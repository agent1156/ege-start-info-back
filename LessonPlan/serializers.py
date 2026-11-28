from rest_framework import serializers
from .models import (
    InfoTopic, 
    LessonDifficulty, 
    ExamType, 
    LessonTag, 
    SchoolClass, 
    LessonPlan
)

# ==========================================
# 1. СЕРИАЛИЗАТОРЫ СПРАВОЧНИКОВ
# ==========================================

class InfoTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoTopic
        fields = ['id', 'title', 'number', 'description', 'slug', 'preview_image']

class LessonDifficultySerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonDifficulty
        fields = ['id', 'title', 'number', 'slug']

class ExamTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamType
        fields = ['id', 'title', 'number', 'slug']

class LessonTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonTag
        fields = ['id', 'title', 'number', 'slug']

class SchoolClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolClass
        fields = ['id', 'title', 'number', 'description', 'slug', 'preview_image']


# ==========================================
# 2. СЕРИАЛИЗАТОР ПЛАНА УРОКА
# ==========================================

class LessonPlanSerializer(serializers.ModelSerializer):
    # Вкладываем связанные объекты, чтобы на фронтенде сразу были названия
    topic = InfoTopicSerializer(read_only=True)
    difficulty = LessonDifficultySerializer(read_only=True)
    exam_type = ExamTypeSerializer(read_only=True)
    tags = LessonTagSerializer(many=True, read_only=True)
    school_classes = SchoolClassSerializer(many=True, read_only=True)

    class Meta:
        model = LessonPlan
        fields = [
            'id', 
            'title', 
            'number', 
            'sort',
            'description', 
            'slug', 
            'preview_image', 
            'detail_image',
            'download_file',
            'topic', 
            'difficulty', 
            'exam_type', 
            'tags', 
            'school_classes'
        ]