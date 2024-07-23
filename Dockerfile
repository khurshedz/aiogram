FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y && pip install -r requirements.txt

COPY . .

COPY init_db.sql /docker-entrypoint-initdb.d/

CMD ["python", "main.py"]
