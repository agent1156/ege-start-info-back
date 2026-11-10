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
    list_display = ('number', 'topic')
    ordering = ('number',)
    search_fields = ('number', 'topic')


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
        'has_image',            # ← теперь проверяет image ИЛИ image_url
        'has_video',
    )
    list_filter = ('task_number', 'year', 'task_type', 'difficulty')
    search_fields = ('external_id', 'text', 'answer', 'image_url')
    list_editable = ('difficulty',)
    list_display_links = ('id', 'external_id')
    ordering = ('-external_id',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Классификация', {
            'fields': ('external_id', 'task_number', 'year', 'task_type', 'difficulty')
        }),
        ('Условие и файлы', {
            'fields': ('text', 'image', 'image_url')
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
        # показываем True, если есть файл ИЛИ ссылка
        return bool(obj.image) or bool(obj.image_url)
    has_image.boolean = True
    has_image.short_description = 'Картинка'

    def has_video(self, obj):
        return bool(obj.video_url)
    has_video.boolean = True
    has_video.short_description = 'Видео'