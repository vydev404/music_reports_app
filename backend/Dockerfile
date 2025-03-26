
FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false

RUN poetry install --no-root

EXPOSE 8000

#CMD uvicorn main:app --host 0.0.0.0 --port 8000 & python worker.py
CMD uvicorn main:app --host 0.0.0.0 --port 8000


