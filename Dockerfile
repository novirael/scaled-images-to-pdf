FROM python:3.11-slim-buster

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY src ./src

RUN poetry install

CMD ["poetry", "run", "python", "./src/app.py"]
