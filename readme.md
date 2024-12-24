# Использование Docker в приложении Flask с БД

### Цель
Реализовать развертывание приложения-счетчика, реализованного в предыдущем задании с использованием с одной из следующих СУБД: Mongo, PostgreSQL, MySQL / Maria DB с использованием Docker Compose

## Отчет

#### Формируем app.py
- Напишем функцию get_db_connection(): для подключения к бд
```
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
```

- Дополним функцию def get_hit_count():
- Получаем информацию о клиенте
```
    client_info = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%d/%b/%Y %H:%M:%S')
```
- Вставляем новую запись
```
cur.execute(
        "INSERT INTO counter_table (datetime, client_info) VALUES (%s, %s)",
        (current_time, client_info)
    )
```

- Получаем общее количество записей
```
  cur.execute("SELECT COUNT(*) FROM counter_table")
    count = cur.fetchone()[0]
```

#### Обновим docker-compose.yml

- Работаем с postgres, поэтому укзываем необходимые для подлключения данные
```
db:
    image: postgres:13-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=counter_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres

volumes:
  postgres_data:
```

#### Сборка
- Создадим таблицу в бд
```
docker-compose exec db psql -U postgres -d counter_db -c "CREATE TABLE counter_table (id SERIAL PRIMARY KEY, datetime VARCHAR(50), client_info TEXT);"
```
- Соберем и запустим приложение
```
docker-compose up --build
```
[![1.png](https://i.postimg.cc/NMhGPPp9/1.png)](https://postimg.cc/DWgKS5Vn)
[![2.png](https://i.postimg.cc/44PZzdkh/2.png)](https://postimg.cc/nMX6xnLH)

#### Результат
- Откроем localhost:5000
[![4.png](https://i.postimg.cc/SNn5JNy4/4.png)](https://postimg.cc/3dH9qh4f)
- Вывбод таблицы
[![3.png](https://i.postimg.cc/QCx26QGK/3.png)](https://postimg.cc/Q9wYCWMj)

