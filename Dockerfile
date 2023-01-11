FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install -r requeriments.txt

ENV PORT 8000

CMD exec uvicorn app:app --host 0.0.0.0 --port $PORT