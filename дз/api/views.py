from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
import hashlib
import json

from .models import InputData, CalculationResult, UserRequest
from .serializers import (
    SegmentTreeRequestSerializer,
    SegmentTreeResponseSerializer,
    UserRequestSerializer,
    InputDataSerializer,
    CalculationResultSerializer
)
import importlib.util
import os

# Импорт модуля с именем, начинающимся с цифры
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("module_339D", os.path.join(base_dir, "339D.py"))
module_339D = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module_339D)
SegmentTree = module_339D.SegmentTree


def get_input_hash(n, array_data):
    """Вычисляет хеш входных данных для проверки уникальности"""
    data_str = json.dumps([n, sorted(array_data)], sort_keys=True)
    return hashlib.sha256(data_str.encode()).hexdigest()


@api_view(['POST'])
def calculate_segment_tree(request):
    """
    API endpoint для вычисления дерева отрезков.
    Проверяет дубликаты входных данных в БД.
    """
    serializer = SegmentTreeRequestSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    n = serializer.validated_data['n']
    array = serializer.validated_data['array']
    updates = serializer.validated_data.get('updates', [])
    
    # Вычисляем хеш входных данных
    input_hash = get_input_hash(n, array)
    
    # Проверяем, есть ли такие входные данные в БД
    input_data_obj = InputData.objects.filter(input_hash=input_hash).first()
    from_cache = False
    
    if input_data_obj:
        # Данные уже есть в БД, получаем результат из БД
        from_cache = True
        result_obj = input_data_obj.result
        initial_result = result_obj.result
        
        # Если есть обновления, нужно пересчитать
        if updates:
            # Создаем дерево из сохраненных данных
            tree = SegmentTree(n, input_data_obj.array_data)
            update_results = []
            
            for update in updates:
                p = update.get('p')
                b = update.get('b')
                if p and b is not None:
                    result = tree.update(p, b)
                    update_results.append(result)
        else:
            update_results = []
    else:
        # Новые входные данные, вычисляем результат
        tree = SegmentTree(n, array)
        initial_result = tree.get_root()
        
        # Выполняем обновления если есть
        update_results = []
        for update in updates:
            p = update.get('p')
            b = update.get('b')
            if p and b is not None:
                result = tree.update(p, b)
                update_results.append(result)
        
        # Сохраняем в БД
        with transaction.atomic():
            input_data_obj = InputData.objects.create(
                n=n,
                array_data=array,
                input_hash=input_hash
            )
            
            result_obj = CalculationResult.objects.create(
                input_data=input_data_obj,
                result=initial_result
            )
    
    # Сохраняем запрос пользователя
    user = request.user if request.user.is_authenticated else None
    ip_address = get_client_ip(request)
    
    UserRequest.objects.create(
        user=user,
        input_data=input_data_obj,
        result=result_obj,
        ip_address=ip_address
    )
    
    # Формируем ответ
    response_data = {
        'initial_result': initial_result,
        'update_results': update_results,
        'from_cache': from_cache,
        'input_data_id': input_data_obj.id,
        'result_id': result_obj.id
    }
    
    response_serializer = SegmentTreeResponseSerializer(data=response_data)
    response_serializer.is_valid()
    
    return Response(response_serializer.validated_data, status=status.HTTP_200_OK)


def get_client_ip(request):
    """Получает IP адрес клиента из запроса"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class UserRequestViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для просмотра истории запросов пользователей"""
    queryset = UserRequest.objects.all()
    serializer_class = UserRequestSerializer
    
    def get_queryset(self):
        queryset = UserRequest.objects.all()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
        return queryset.order_by('-timestamp')


class InputDataViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для просмотра входных данных"""
    queryset = InputData.objects.all()
    serializer_class = InputDataSerializer


class CalculationResultViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для просмотра результатов вычислений"""
    queryset = CalculationResult.objects.all()
    serializer_class = CalculationResultSerializer
