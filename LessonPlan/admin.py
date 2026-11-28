from django.contrib import admin
from .models import (
    InfoTopic, 
    LessonDifficulty, 
    ExamType, 
    LessonTag, 
    SchoolClass, 
    LessonPlan
)

# ==========================================
# 1. СПРАВОЧНИКИ
# ==========================================

@admin.register(InfoTopic)
class InfoTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'number', 'sort', 'is_active')
    list_editable = ('sort', 'is_active')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(LessonDifficulty)
class LessonDifficultyAdmin(admin.ModelAdmin):
    list_display = ('title', 'number', 'sort', 'is_active')
    list_editable = ('sort', 'is_active')
    search_fields = ('title',)

@admin.register(ExamType)
class ExamTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'number', 'sort', 'is_active')
    list_editable = ('sort', 'is_active')
    search_fields = ('title',)

@admin.register(LessonTag)
class LessonTagAdmin(admin.ModelAdmin):
    list_display = ('title', 'number', 'sort', 'is_active')
    list_editable = ('sort', 'is_active')
    search_fields = ('title',)

# НОВАЯ РЕГИСТРАЦИЯ: КЛАССЫ
@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'number', 'sort', 'is_active')
    list_editable = ('sort', 'is_active')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}


# ==========================================
# 2. ПЛАНЫ УРОКОВ (Основная модель)
# ==========================================

@admin.register(LessonPlan)
class LessonPlanAdmin(admin.ModelAdmin):
    # Что показываем в общем списке
    list_display = (
        'title', 
        'number', 
        'topic', 
        'difficulty', 
        'exam_type', 
        'sort', 
        'is_active'
    )
    
    # Фильтры справа
    list_filter = ('topic', 'difficulty', 'exam_type', 'school_classes', 'is_active')
    
    # Поиск
    search_fields = ('title', 'description')
    
    # Возможность менять сортировку и активность прямо из списка
    list_editable = ('sort', 'is_active')
    
    # Удобный виджет для выбора тегов и классов
    filter_horizontal = ('tags', 'school_classes')
    
    # Группировка полей в карточке редактирования
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'number', 'description', 'sort', 'is_active')
        }),
        ('Связи', {
            'fields': ('topic', 'difficulty', 'exam_type', 'tags', 'school_classes')
        }),
        ('Медиа и файлы', {
            'fields': ('preview_image', 'detail_image', 'download_file', 'slug')
        }),
    )