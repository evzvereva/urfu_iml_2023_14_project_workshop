FROM python:3.11.7-slim
WORKDIR /app
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p domain
COPY domain domain
RUN mkdir -p service
COPY service service
COPY gpt-api.py .
COPY secrets.txt .
COPY settings.yaml .
RUN mkdir logs
CMD ["uvicorn", "gpt-api:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]
