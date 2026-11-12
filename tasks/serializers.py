from rest_framework import serializers
from .models import Task, TaskNumber

# Вложенный сериализатор для задач внутри задания
class TaskListSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField(source='year.year', read_only=True, allow_null=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id', 'external_id', 'text', 'answer', 'image', 'year')

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            url = obj.image.url
            return request.build_absolute_uri(url) if request else url
        return obj.image_url or ''

# Основной сериализатор задания
class TaskNumberSerializer(serializers.ModelSerializer):
    tasks = TaskListSerializer(many=True, read_only=True) # Подтягиваем все задачи

    class Meta:
        model = TaskNumber
        fields = ('number', 'topic', 'max_score', 'slug', 'tasks')

# Старый сериализатор для списка задач (оставляем)
class TaskSerializer(serializers.ModelSerializer):
    task_number = serializers.IntegerField(source='task_number.number', read_only=True)
    task_slug = serializers.CharField(source='task_number.slug', read_only=True)
    max_score = serializers.IntegerField(source='task_number.max_score', read_only=True)
    task_topic = serializers.CharField(source='task_number.topic', read_only=True)
    year = serializers.IntegerField(source='year.year', read_only=True, allow_null=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            'id', 'external_id', 'task_number', 'task_slug', 'max_score', 
            'task_topic', 'year', 'text', 'answer', 'image', 'image_url', 'video_url',
        )

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            url = obj.image.url
            return request.build_absolute_uri(url) if request else url
        return obj.image_url or ''