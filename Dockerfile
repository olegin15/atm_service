FROM python:3.7
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app/
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV DJANGO_SETTINGS_MODULE=project.settings

CMD python manage.py collectstatic --noinput && \
    python manage.py migrate && \
    python manage.py runserver 0.0.0.0:8000