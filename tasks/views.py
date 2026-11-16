from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Task, TaskNumber, TaskYear, TaskType, TaskDifficulty
from .serializers import TaskSerializer, TaskNumberSerializer


class TaskNumberViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Эндпоинт для главной страницы: отдает все 27 заданий.
    """
    queryset = TaskNumber.objects.all()
    serializer_class = TaskNumberSerializer
    pagination_class = None


class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Эндпоинт для задач с фильтрацией.
    """
    serializer_class = TaskSerializer
    pagination_class = PageNumberPagination
    queryset = Task.objects.all()

    def get_queryset(self):
        qs = Task.objects.select_related('task_number', 'year', 'task_type', 'difficulty').order_by('-external_id')

        task_slug = self.request.query_params.get('task_slug')
        if task_slug:
            qs = qs.filter(task_number__slug=task_slug)

        year = self.request.query_params.get('year')
        if year:
            qs = qs.filter(year__year=year)

        task_type = self.request.query_params.get('type')
        if task_type:
            qs = qs.filter(task_type__name=task_type)

        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            qs = qs.filter(difficulty__name=difficulty)

        return qs


class FilterOptionsView(APIView):
    """
    Эндпоинт для получения доступных фильтров.
    Возвращает только те года, типы и сложности, которые реально есть в базе.
    """
    def get(self, request):
        # Достаем уникальные значения из связанных таблиц
        years = TaskYear.objects.all().order_by('-year').values_list('year', flat=True)
        types = TaskType.objects.all().values_list('name', flat=True)
        difficulties = TaskDifficulty.objects.all().values_list('name', flat=True)

        return Response({
            'years': list(years),
            'types': list(types),
            'difficulties': list(difficulties)
        })