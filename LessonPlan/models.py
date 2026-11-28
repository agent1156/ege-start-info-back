from django.db import models
from django.utils.text import slugify
from pytils.translit import slugify as ru_slugify


# ==========================================
# БАЗОВАЯ МОДЕЛЬ (Абстрактная)
# ==========================================
class BaseCatalogModel(models.Model):
    """
    Абстрактная модель, от которой будут наследоваться все справочники.
    Содержит общие поля для сортировки, активности и картинок.
    """
    sort = models.PositiveSmallIntegerField(
        default=0, 
        verbose_name='Порядок сортировки',
        help_text='Чем меньше число, тем выше элемент в списке'
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name='Активно',
        help_text='Если снять галочку, элемент скроется с сайта'
    )
    number = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Номер',
        help_text='Номер для отображения (например, 1, 2, 3)'
    )
    description = models.TextField(
        blank=True, 
        default='', 
        verbose_name='Описание'
    )
    preview_image = models.ImageField(
        upload_to='catalog/previews/', 
        blank=True, 
        null=True,
        verbose_name='Картинка превью',
        help_text='Небольшая картинка для списка'
    )
    detail_image = models.ImageField(
        upload_to='catalog/details/', 
        blank=True, 
        null=True,
        verbose_name='Картинка детальная',
        help_text='Большая картинка для страницы'
    )
    title = models.CharField(
        max_length=255, 
        blank=True, 
        default='', 
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=255, 
        unique=True,
        blank=True,
        verbose_name='ЧПУ (URL)',
        help_text='Генерируется автоматически'
    )

    class Meta:
        abstract = True # Django не будет создавать таблицу для этой модели
        ordering = ['sort', 'number']

    def save(self, *args, **kwargs):
        # Автогенерация слага, если его нет
        if not self.slug:
            base_text = self.title if self.title else "item"
            transliterated = ru_slugify(base_text)
            self.slug = slugify(transliterated)
            # Защита от дублей слагов (добавляем номер, если слаг уже занят)
            if self.__class__.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                self.slug = f"{self.slug}-{self.number}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.number}. {self.title}"


# ==========================================
# 1. СПРАВОЧНИКИ
# ==========================================

class InfoTopic(BaseCatalogModel):
    """Темы информатики"""
    class Meta(BaseCatalogModel.Meta):
        verbose_name = 'Тема информатики'
        verbose_name_plural = 'Темы информатики'


class LessonDifficulty(BaseCatalogModel):
    """Уровень сложности урока"""
    class Meta(BaseCatalogModel.Meta):
        verbose_name = 'Уровень сложности'
        verbose_name_plural = 'Уровни сложности'


class ExamType(BaseCatalogModel):
    """Тип экзамена (ЕГЭ или ОГЭ)"""
    class Meta(BaseCatalogModel.Meta):
        verbose_name = 'Тип экзамена (ЕГЭ/ОГЭ)'
        verbose_name_plural = 'Типы экзаменов'


class LessonTag(BaseCatalogModel):
    """Теги к урокам"""
    class Meta(BaseCatalogModel.Meta):
        verbose_name = 'Тег урока'
        verbose_name_plural = 'Теги уроков'


class SchoolClass(BaseCatalogModel):
    """Справочник классов (например, 10 класс, 11 класс)"""
    class Meta(BaseCatalogModel.Meta):
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'


# ==========================================
# 2. ПЛАН УРОКА (Основная модель)
# ==========================================

class LessonPlan(BaseCatalogModel):
    """План урока по информатике"""
    
    # Внешние ключи (Ссылки на другие таблицы)
    topic = models.ForeignKey(
        InfoTopic,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lesson_plans',
        verbose_name='Тема информатики'
    )
    difficulty = models.ForeignKey(
        LessonDifficulty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lesson_plans',
        verbose_name='Уровень сложности'
    )
    exam_type = models.ForeignKey(
        ExamType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lesson_plans',
        verbose_name='Тип экзамена (ЕГЭ/ОГЭ)'
    )
    
    # Связи ManyToMany
    tags = models.ManyToManyField(
        LessonTag,
        blank=True,
        related_name='lesson_plans',
        verbose_name='Теги'
    )
    school_classes = models.ManyToManyField(
        SchoolClass,
        blank=True,
        related_name='lesson_plans',
        verbose_name='Классы',
        help_text='Для каких классов подходит этот урок'
    )

    # Дополнительные поля
    download_file = models.FileField(
        upload_to='lessons/files/',
        blank=True,
        null=True,
        verbose_name='Файл для скачивания',
        help_text='Конспект, материалы или архив с задачами'
    )

    # Переопределяем Meta для более точного названия
    class Meta(BaseCatalogModel.Meta):
        verbose_name = 'План урока'
        verbose_name_plural = 'Планы уроков'
        ordering = ['sort', 'number']

    def __str__(self):
        return f"Урок {self.number}: {self.title}"