from django.contrib import admin
from .models import Task, TaskNumber, TaskYear, TaskType, TaskDifficulty

# Регистрируем справочники
admin.site.register(TaskYear)
admin.site.register(TaskType)

@admin.register(TaskDifficulty)
class TaskDifficultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')

@admin.register(TaskNumber)
class TaskNumberAdmin(admin.ModelAdmin):
    list_display = ('number', 'topic')
    ordering = ('number',)

# Регистрируем задачи
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'task_number', 'year', 'task_type', 'difficulty', 'has_image', 'has_video')
    list_filter = ('task_number', 'year', 'task_type', 'difficulty')
    search_fields = ('text', 'answer')
    list_editable = ('difficulty',)
    
    fieldsets = (
        ('Классификация', {
            'fields': ('task_number', 'year', 'task_type', 'difficulty')
        }),
        ('Условие и файлы', {
            'fields': ('text', 'image')
        }),
        ('Решение', {
            'fields': ('answer', 'video_url')
        }),
    )

    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True

    def has_video(self, obj):
        return bool(obj.video_url)
    has_video.boolean = True