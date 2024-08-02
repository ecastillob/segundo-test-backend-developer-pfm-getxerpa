FROM python:3.12

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install poetry

RUN mkdir /code
RUN mkdir /static

WORKDIR /code
COPY poetry.lock pyproject.toml /code/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --without dev

COPY . /code/
WORKDIR /code/src

RUN python manage.py collectstatic --noinput
