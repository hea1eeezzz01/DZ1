# Быстрый старт

## Установка и запуск

1. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

2. **Создайте миграции и примените их:**
```bash
python manage.py makemigrations
python manage.py migrate
```

3. **Создайте суперпользователя (опционально):**
```bash
python manage.py createsuperuser
```

4. **Запустите сервер:**
```bash
python manage.py runserver
```

5. **Откройте в браузере:**
- Главная страница: http://127.0.0.1:8000/
- Админ-панель: http://127.0.0.1:8000/admin/
- API: http://127.0.0.1:8000/api/

## Пример использования API

```bash
curl -X POST http://127.0.0.1:8000/api/calculate/ \
  -H "Content-Type: application/json" \
  -d '{
    "n": 2,
    "array": [1, 2, 3, 4],
    "updates": [{"p": 1, "b": 4}]
  }'
```

## Тестирование

```bash
python -m unittest test_339D.py
```
