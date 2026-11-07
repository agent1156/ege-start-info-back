from django.db import models

class ContactRequest(models.Model):
    """Модель для заявок с формы обратной связи"""
    
    name = models.CharField(
        max_length=255, 
        verbose_name='Имя'
    )
    phone = models.CharField(
        max_length=50, 
        verbose_name='Телефон'
    )
    email = models.EmailField(
        verbose_name='Почта'
    )
    message = models.TextField(
        verbose_name='Ваше сообщение'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Дата создания'
    )
    is_processed = models.BooleanField(
        default=False, 
        verbose_name='Обработана'
    )

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at'] # Сначала новые

    def __str__(self):
        return f'{self.name} ({self.phone}) - {self.created_at.strftime("%d.%m.%Y %H:%M")}'