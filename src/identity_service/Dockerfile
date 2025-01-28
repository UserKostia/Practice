#FROM ubuntu:latest
#LABEL authors="Kostia"
#
#ENTRYPOINT ["top", "-b"]

# Використання офіційного Python образу
FROM python:3.11-slim-bullseye

# Встановлення змінних середовища
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME /app

# Створення робочої директорії
WORKDIR $APP_HOME

# Встановлення системних залежностей
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копіювання файлів залежностей
COPY pyproject.toml poetry.lock* ./

# Встановлення Poetry та залежностей
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Копіювання коду додатку
COPY . .

# Встановлення портів та точки входу
EXPOSE 8000

# Запуск додатку через Gunicorn
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "src.identity_service.app.main:app"]