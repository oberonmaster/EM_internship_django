# Dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN apt-get update && apt-get install -y netcat-openbsd
RUN pip install --upgrade pip && pip install -r requirements.txt


# Копируем весь проект (включая entrypoint.sh)
COPY . .

# Делаем скрипт исполняемым
RUN chmod +x entrypoint.sh
