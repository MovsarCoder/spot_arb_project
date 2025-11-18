FROM python:3.11-slim

# Установка рабочей директории
WORKDIR /app

# Копирование файлов зависимостей
COPY tg_bot/requirements.txt .

# Установка зависимостей Python
RUN pip install -r requirements.txt

# Копирование исходного кода tg_bot
COPY tg_bot ./tg_bot

# Копирование парсеров
COPY parser ./parser

# Создание директории для базы данных
RUN mkdir -p /app/database

# Установка PYTHONPATH для правильной работы импортов
ENV PYTHONPATH=/app

# Команда для запуска приложения
CMD ["python", "tg_bot/main.py"]