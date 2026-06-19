FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=configuracao.settings

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/api

COPY api/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY api/ .
COPY sistema_web/templates/ ./templates/
COPY sistema_web/static/ ./static/

RUN mkdir -p /app/api/staticfiles /app/api/media

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn configuracao.wsgi:application --bind 0.0.0.0:8000"]
