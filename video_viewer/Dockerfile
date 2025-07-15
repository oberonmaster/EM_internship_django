# Dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

# Выполняем миграции и запускаем gunicorn
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn video_viewer.wsgi:application --bind 0.0.0.0:8000"]
