#!/bin/sh

echo "Waiting for Postgres..."

# Ждем, пока Postgres не станет доступен
while ! nc -z db 5432; do
  sleep 1
done

echo "Postgres is up - continuing..."

# Миграции и сбор статики
python manage.py migrate
python manage.py collectstatic --noinput

# Создаем суперпользователя, если он еще не создан
echo "Creating superuser if it doesn't exist..."

python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
END


# Автозаполнение базы
# TODO закомментировать
python manage.py generate_fake_data


# Запускаем сервер через gunicorn
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
