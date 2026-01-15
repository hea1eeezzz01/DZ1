from rest_framework import serializers
from .models import InputData, CalculationResult, UserRequest
from django.contrib.auth.models import User


class InputDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = InputData
        fields = ['id', 'n', 'array_data', 'created_at']


class CalculationResultSerializer(serializers.ModelSerializer):
    input_data = InputDataSerializer(read_only=True)
    
    class Meta:
        model = CalculationResult
        fields = ['id', 'input_data', 'result', 'created_at']


class UserRequestSerializer(serializers.ModelSerializer):
    input_data = InputDataSerializer(read_only=True)
    result = CalculationResultSerializer(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True, allow_null=True)
    
    class Meta:
        model = UserRequest
        fields = ['id', 'user', 'username', 'input_data', 'result', 'timestamp', 'ip_address']


class SegmentTreeRequestSerializer(serializers.Serializer):
    """Сериализатор для запроса вычисления дерева отрезков"""
    n = serializers.IntegerField(min_value=0, max_value=20)
    array = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1
    )
    updates = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField()
        ),
        required=False,
        allow_empty=True
    )
    
    def validate(self, data):
        n = data['n']
        array = data['array']
        expected_length = 1 << n  # 2^n
        
        if len(array) != expected_length:
            raise serializers.ValidationError(
                f"Длина массива должна быть {expected_length} (2^{n}), получено {len(array)}"
            )
        
        return data


class SegmentTreeResponseSerializer(serializers.Serializer):
    """Сериализатор для ответа с результатами вычислений"""
    initial_result = serializers.IntegerField()
    update_results = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )
    from_cache = serializers.BooleanField()
    input_data_id = serializers.IntegerField()
    result_id = serializers.IntegerField()
