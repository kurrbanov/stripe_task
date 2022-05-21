FROM python:3.9
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt install vim -y

WORKDIR /usr/src/
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --system

COPY . ./
CMD python wait-postgres.py && \
    python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py shell < fill_db.py && \
    python manage.py runserver 0.0.0.0:8000