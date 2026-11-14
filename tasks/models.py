from django.db import models
from django.utils.text import slugify
from pytils.translit import slugify as ru_slugify 


# ==========================================
# 1. СПРАВОЧНИКИ (Связанные таблицы)
# ==========================================

class TaskYear(models.Model):
    """Справочник годов задач (ЕГЭ 2025, 2026 и т.д.)"""
    
    year = models.PositiveSmallIntegerField(
        unique=True, 
        verbose_name='Год'
    )

    class Meta:
        verbose_name = 'Год задачи'
        verbose_name_plural = 'Годы задач'
        ordering = ['-year']  # Сначала новые

    def __str__(self):
        return str(self.year)


class TaskType(models.Model):
    """Справочник типов задач (ЕГЭ, ОГЭ, Олимпиада)"""
    
    name = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name='Тип задачи'
    )

    class Meta:
        verbose_name = 'Тип задачи'
        verbose_name_plural = 'Типы задач'
        ordering = ['name']

    def __str__(self):
        return self.name


class TaskDifficulty(models.Model):
    """Справочник уровней сложности"""
    
    name = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name='Уровень сложности'
    )
    
    color = models.CharField(
        max_length=7, 
        default='#64748b', 
        verbose_name='Цвет (HEX)',
        help_text='Например: #10b981 (зеленый)'
    )

    class Meta:
        verbose_name = 'Сложность'
        verbose_name_plural = 'Уровни сложности'
        ordering = ['id']

    def __str__(self):
        return self.name


class TaskNumber(models.Model):
    """Справочник номеров заданий ЕГЭ (1-27)"""
    
    number = models.PositiveSmallIntegerField(
        unique=True, 
        verbose_name='Номер задания (1-27)'
    )
    
    topic = models.CharField(
        max_length=255, 
        blank=True, 
        verbose_name='Тема задания',
        help_text='Например: Графы, Логика, Программирование'
    )

    max_score = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Первичный балл',
        help_text='Сколько баллов дают за это задание'
    )

    slug = models.SlugField(
        max_length=255, 
        unique=True,   # <-- Включили уникальность
        blank=True,    # <-- Разрешили быть пустым (заполнится автоматически)
        verbose_name='ЧПУ (URL)',
        help_text='Например: 1-analiz-modeley'
    )

    class Meta:
        verbose_name = 'Номер задания'
        verbose_name_plural = 'Номера заданий (справочник)'
        ordering = ['number']

    def __str__(self):
        if self.topic:
            return f'Задание {self.number}: {self.topic}'
        return f'Задание {self.number}'

    def save(self, *args, **kwargs):
        # Автогенерация слага, если он пустой
        if not self.slug:
            # 1. Берем тему (или пустую строку, если темы нет)
            base_text = self.topic if self.topic else "zadanie"
            
            # 2. Транслитерация (Привет -> privet)
            transliterated = ru_slugify(base_text)
            
            # 3. Очистка от спецсимволов и генерация слага
            self.slug = slugify(transliterated)
            
        super().save(*args, **kwargs)

# ==========================================
# 2. ОСНОВНАЯ МОДЕЛЬ ЗАДАЧИ
# ==========================================

class Task(models.Model):
    """Модель для задач ЕГЭ"""
    
    # ===== СВЯЗИ (Внешние ключи) =====
    task_number = models.ForeignKey(
        TaskNumber, 
        on_delete=models.CASCADE, 
        related_name='tasks',
        verbose_name='Номер задания'
    )
    
    year = models.ForeignKey(
        TaskYear, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='tasks',
        verbose_name='Год задачи'
    )
    
    task_type = models.ForeignKey(
        TaskType, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='tasks',
        verbose_name='Тип задачи'
    )
    
    difficulty = models.ForeignKey(
        TaskDifficulty, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='tasks',
        verbose_name='Сложность'
    )

    # ===== НОВЫЕ ПОЛЯ ДЛЯ ПАРСЕРА =====
    external_id = models.PositiveIntegerField(
        unique=True,
        null=True,
        blank=True,
        db_index=True,
        verbose_name='ID на источнике',
        help_text='Номер задачи на kpolyakov.spb.ru (например, 9296)'
    )

    image_url = models.URLField(
        max_length=500,
        blank=True,
        default='',
        verbose_name='Ссылка на картинку (источник)',
        help_text='Прямая ссылка на .gif/.png с сайта-источника'
    )

    # ===== ОСНОВНЫЕ ПОЛЯ =====
    text = models.TextField(
        verbose_name='Текст задачи'
    )

    image = models.ImageField(
        upload_to='tasks/files/', 
        verbose_name='Прикрепленный файл (картинка)', 
        blank=True, 
        null=True,
        help_text='Схема, график, таблица и т.д.'
    )
    attachment = models.FileField(
        upload_to='tasks/attachments/',
        verbose_name='Файл для решения',
        blank=True,
        null=True,
        help_text='Документ, таблица или архив с данными для задачи'
    )

    answer = models.CharField(
        max_length=255, 
        verbose_name='Ответ',
        blank=True,
        default=''
    )

    video_url = models.URLField(
        max_length=500,
        blank=True, 
        null=True,
        verbose_name='Ссылка на видео с решением',
        help_text='Например: https://youtu.be/...'
    )

    # ===== МЕТАДАННЫЕ =====
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Дата добавления'
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'База задач'
        ordering = ['task_number__number', '-created_at']

    def __str__(self):
        return f'Задача {self.task_number.number} (ID: {self.id})'