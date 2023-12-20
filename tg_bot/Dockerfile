FROM python:3.9.18-slim

LABEL desc="TG Bot для Проектной практики УрФУ МЛ 2023. Подгруппа 14"
LABEL authors="MulyavinAA"
LABEL version="0.1"

# Отключение буффера для вывода в консоль
ENV PYTHONUNBUFFERED=1
# Отключение создание файлов с байткодом *.pyc
ENV PYTHONDONTWRITEBYTECODE=1

# Установка рабочего каталога
WORKDIR /tg_bot_pp14

# Копирование файлов приложения
COPY ./src/ ./
COPY ./requirements.txt ./

# Установка зависимостей для приложения
RUN pip install --no-cache-dir -r ./requirements.txt

# Запуск приложения
CMD ["python", "./main.py"]
