FROM python:3.10

RUN mkdir /app
COPY . /app
COPY pyproject.toml /app

WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
RUN pip install psycopg2

CMD ["python", "main.py"]