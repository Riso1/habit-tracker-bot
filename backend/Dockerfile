FROM python:3.11-slim

WORKDIR /code

RUN pip install --upgrade pip
RUN pip install poetry

COPY pyproject.toml .

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

COPY . .
