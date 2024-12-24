from flask import Flask, request
from datetime import datetime
import psycopg2
import time
import os

app = Flask(__name__)

def get_db_connection():
    retries = 5
    while True:
        try:
            conn = psycopg2.connect(
                host='db',
                database='counter_db',
                user='postgres',
                password='postgres'
            )
            return conn
        except psycopg2.OperationalError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def get_hit_count():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Получаем информацию о клиенте
    client_info = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%d/%b/%Y %H:%M:%S')
    
    # Вставляем новую запись
    cur.execute(
        "INSERT INTO counter_table (datetime, client_info) VALUES (%s, %s)",
        (current_time, client_info)
    )
    
    # Получаем общее количество записей
    cur.execute("SELECT COUNT(*) FROM counter_table")
    count = cur.fetchone()[0]
    
    conn.commit()
    cur.close()
    conn.close()
    
    return count

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)