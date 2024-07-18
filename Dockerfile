FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

COPY init.sql /docker-entrypoint-initdb.d/

# запуска инициализации и приложения
CMD ["sh", "-c", "psql -U $POSTGRES_USER -d $POSTGRES_DB -a -f /docker-entrypoint-initdb.d/init_db.sql && python main.py"]
