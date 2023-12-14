FROM python:3.9.18-slim

LABEL desc="TG Bot для Проектной практики УрФУ МЛ 2023. Подгруппа 14"
LABEL authors="MulyavinAA"
LABEL version="0.1"

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /tg_bot_pp14

COPY ./src/ ./
COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r ./requirements.txt

CMD ["python", "./main.py"]