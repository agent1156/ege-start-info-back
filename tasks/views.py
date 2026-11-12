from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Task, TaskNumber
from .serializers import TaskSerializer, TaskNumberSerializer


class TaskNumberViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Эндпоинт для главной страницы: отдает все 27 заданий (тема, балл, слаг).
    Пример: GET /api/task-numbers/
    """
    queryset = TaskNumber.objects.all()
    serializer_class = TaskNumberSerializer
    pagination_class = None # Отключаем пагинацию, чтобы отдать все 27


class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Эндпоинт для детальной страницы: отдает задачи.
    Пример: GET /api/tasks/?task_slug=analiz-informatsionnyih-modelej
    """
    serializer_class = TaskSerializer
    pagination_class = PageNumberPagination
    queryset = Task.objects.all() # Нужно для DRF

    def get_queryset(self):
        qs = Task.objects.select_related('task_number', 'year').order_by('-external_id')

        # 1. Фильтр по слагу задания (используется на детальной странице /tasks/[slug])
        task_slug = self.request.query_params.get('task_slug')
        if task_slug:
            qs = qs.filter(task_number__slug=task_slug)

        # 2. Фильтр по номеру задания (например, ?task_number=1)
        task_number = self.request.query_params.get('task_number')
        if task_number:
            qs = qs.filter(task_number__number=task_number)

        # 3. Поиск по тексту задачи (для строки поиска)
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(Q(text__icontains=search) | Q(answer__icontains=search))

        # 4. Фильтр по году
        year = self.request.query_params.get('year')
        if year:
            qs = qs.filter(year__year=year)

        return qs