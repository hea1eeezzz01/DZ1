from django.contrib import admin
from .models import InputData, CalculationResult, UserRequest


@admin.register(InputData)
class InputDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'n', 'array_data', 'input_hash', 'created_at']
    list_filter = ['n', 'created_at']
    search_fields = ['input_hash', 'array_data']
    readonly_fields = ['input_hash', 'created_at']


@admin.register(CalculationResult)
class CalculationResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'input_data', 'result', 'created_at']
    list_filter = ['created_at']
    search_fields = ['result']
    readonly_fields = ['created_at']


@admin.register(UserRequest)
class UserRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'input_data', 'result', 'timestamp', 'ip_address']
    list_filter = ['timestamp', 'user']
    search_fields = ['user__username', 'ip_address']
    readonly_fields = ['timestamp']
