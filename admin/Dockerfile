FROM python:3.10

RUN mkdir /admin
COPY . /admin

WORKDIR /admin
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip install fastapi sqlalchemy sqladmin python-dotenv psycopg2 uvicorn

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
# CMD ["uvicorn", "main:app", "--port", "8080"]