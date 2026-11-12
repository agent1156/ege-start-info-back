from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Task, TaskNumber
from .serializers import TaskSerializer, TaskNumberSerializer

class TaskNumberPagination(PageNumberPagination):
    page_size = 50 # Выведем много задач на страницу задания

class TaskNumberViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Эндпоинт для получения информации о задании и списка его задач.
    Пример: GET /api/task-numbers/analiz-informatsionnyh-modeley-grafy-tablitsy/
    """
    queryset = TaskNumber.objects.all()
    serializer_class = TaskNumberSerializer
    pagination_class = None # Отключаем пагинацию, чтобы получить все 27 заданий разом для главной
    
    # Говорим Django искать не по ID, а по slug
    lookup_field = 'slug'


class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Эндпоинт для получения списка задач.
    Пример: GET /api/tasks/?task_number=analiz-informatsionnyh-modeley-grafy-tablitsy
    """
    serializer_class = TaskSerializer
    pagination_class = TaskNumberPagination
    queryset = Task.objects.all()

    def get_queryset(self):
        qs = Task.objects.select_related('task_number', 'year').order_by('-external_id')

        # Фильтрация по слагу задания (используется на детальной странице)
        task_slug = self.request.query_params.get('task_slug')
        if task_slug:
            qs = qs.filter(task_number__slug=task_slug)

        # Старые фильтры
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(Q(text__icontains=search) | Q(answer__icontains=search))
            
        year = self.request.query_params.get('year')
        if year:
            qs = qs.filter(year__year=year)

        task_number = self.request.query_params.get('task_number')
        if task_number:
            qs = qs.filter(task_number__number=task_number)

        return qs