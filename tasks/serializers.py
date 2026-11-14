from rest_framework import serializers
from .models import Task, TaskNumber


# 1. Сериализатор для одной задачи (используется внутри задания и в общем списке)
class TaskSerializer(serializers.ModelSerializer):
    # Достаем данные из связанной таблицы TaskNumber
    task_number = serializers.IntegerField(source='task_number.number', read_only=True)
    task_slug = serializers.CharField(source='task_number.slug', read_only=True)
    max_score = serializers.IntegerField(source='task_number.max_score', read_only=True)
    task_topic = serializers.CharField(source='task_number.topic', read_only=True)
    
    # Достаем год из связанной таблицы TaskYear
    year = serializers.IntegerField(source='year.year', read_only=True, allow_null=True)
    
    # Кастомные поля
    image = serializers.SerializerMethodField()
    attachment = serializers.SerializerMethodField() 

    class Meta:
        model = Task
        fields = (
            'id', 'external_id', 'task_number', 'task_slug', 'max_score', 
            'task_topic', 'year', 'text', 'answer', 'image', 'image_url', 'attachment','video_url',
        )

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            url = obj.image.url
            return request.build_absolute_uri(url) if request else url
        return obj.image_url or ''

    # ===== ВОТ ЭТОГО МЕТОДА НЕ ХВАТАЛО =====
    def get_attachment(self, obj):
        if obj.attachment:
            request = self.context.get('request')
            url = obj.attachment.url
            return request.build_absolute_uri(url) if request else url
        return None


# 2. Сериализатор для справочника заданий (для главной страницы с 27 карточками)
class TaskNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskNumber
        fields = ('number', 'topic', 'max_score', 'slug')