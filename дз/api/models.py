from django.db import models
from django.contrib.auth.models import User
import json


class InputData(models.Model):
    """Модель для хранения уникальных входных данных"""
    n = models.IntegerField(verbose_name='Степень двойки')
    array_data = models.JSONField(verbose_name='Массив данных')
    input_hash = models.CharField(max_length=64, unique=True, db_index=True, verbose_name='Хеш входных данных')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Входные данные'
        verbose_name_plural = 'Входные данные'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"n={self.n}, array={self.array_data[:10]}..."
    
    def save(self, *args, **kwargs):
        # Создаем хеш для проверки уникальности
        if not self.input_hash:
            data_str = json.dumps([self.n, sorted(self.array_data)], sort_keys=True)
            import hashlib
            self.input_hash = hashlib.sha256(data_str.encode()).hexdigest()
        super().save(*args, **kwargs)


class CalculationResult(models.Model):
    """Модель для хранения результатов вычислений"""
    input_data = models.OneToOneField(InputData, on_delete=models.CASCADE, related_name='result', verbose_name='Входные данные')
    result = models.IntegerField(verbose_name='Результат')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата вычисления')
    
    class Meta:
        verbose_name = 'Результат вычисления'
        verbose_name_plural = 'Результаты вычислений'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Result: {self.result}"


class UserRequest(models.Model):
    """Модель для хранения запросов пользователей"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')
    input_data = models.ForeignKey(InputData, on_delete=models.CASCADE, related_name='requests', verbose_name='Входные данные')
    result = models.ForeignKey(CalculationResult, on_delete=models.CASCADE, related_name='user_requests', verbose_name='Результат')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время запроса')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP адрес')
    
    class Meta:
        verbose_name = 'Запрос пользователя'
        verbose_name_plural = 'Запросы пользователей'
        ordering = ['-timestamp']
    
    def __str__(self):
        username = self.user.username if self.user else 'Анонимный'
        return f"{username} - {self.timestamp}"
