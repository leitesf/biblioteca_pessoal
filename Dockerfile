ARG PYTHON_VERSION=3.10-slim-buster

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

RUN pip install pipenv
COPY Pipfile Pipfile.lock /code/
RUN pipenv install --deploy --system

COPY . /code
RUN pip install -r requirements.txt

ENV SECRET_KEY "non-secret-key-for-building-purposes"  # <-- Updated!
RUN python manage.py collectstatic --noinput
RUN python manage.py loaddata main/fixtures/grupos.json
RUN python manage.py loaddata games/fixtures/cadastros.json
EXPOSE 8000

# TODO: replace demo.wsgi with <project_name>.wsgi
CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "biblioteca_pessoal.wsgi"]
