FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

COPY init_db.sql /docker-entrypoint-initdb.d/

CMD ["python", "main.py"]
