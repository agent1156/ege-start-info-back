from django.contrib import admin
from .models import Task, TaskNumber, TaskYear, TaskType, TaskDifficulty


# ============ Справочники ============

admin.site.register(TaskYear)
admin.site.register(TaskType)


@admin.register(TaskDifficulty)
class TaskDifficultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')


@admin.register(TaskNumber)
class TaskNumberAdmin(admin.ModelAdmin):
    # 'number' должен быть первым, так как он служит ссылкой на редактирование.
    list_display = ('number', 'title', 'order', 'topic', 'max_score', 'slug', 'is_active')
    
    # Позволяет менять поле order и is_active прямо в общем списке
    list_editable = ('order', 'is_active')
    
    # Добавляем фильтры и поиск
    list_filter = ('max_score', 'is_active')
    search_fields = ('title', 'number', 'topic', 'slug')
    
    # Группируем поля в форме редактирования
    fieldsets = (
        ('Основная информация', {
            # ВОТ ЗДЕСЬ БЫЛА ОШИБКА — ТЕПЕРЬ ЗАПЯТАЯ НА МЕСТЕ
            'fields': ('number', 'order', 'title', 'topic', 'is_active')
        }),
        ('Настройки ЕГЭ', {
            'fields': ('max_score', 'slug'),
            'description': 'Первичный балл и ЧПУ (генерируется автоматически, если оставить пустым)'
        }),
    )
    
    # Сортируем сначала по order, а если order одинаковый — по number
    ordering = ('order', 'number')


# ============ Задачи ============

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'external_id',          # ← номер с сайта-источника
        'task_number',
        'year',
        'task_type',
        'difficulty',
        'answer',
        'has_image',            # ← проверяет image ИЛИ image_url
        'has_video',
        'is_active',
    )
    list_filter = ('task_number', 'year', 'task_type', 'difficulty', 'is_active')
    search_fields = ('external_id', 'text', 'answer', 'image_url')
    list_editable = ('difficulty', 'is_active')
    list_display_links = ('id', 'external_id')
    ordering = ('-external_id',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Классификация', {
            'fields': ('external_id', 'task_number', 'year', 'task_type', 'difficulty', 'is_active')
        }),
        ('Условие и файлы', {
            'fields': ('text', 'image', 'attachment', 'image_url')
        }),
        ('Решение', {
            'fields': ('answer', 'video_url')
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def has_image(self, obj):
        return bool(obj.image) or bool(obj.image_url)
    has_image.boolean = True
    has_image.short_description = 'Картинка'

    def has_video(self, obj):
        return bool(obj.video_url)
    has_video.boolean = True
    has_video.short_description = 'Видео'