# Тестовое задание MEDIASOFT

- ФИО
- RestAPI сервис, реализующий взаимодействие с базой данных блога по HTTP(s)

## Установка и запуск
1. Создать виртуальное окружение ```python3 -m venv venv``` и активировать его ```source ./venv/bin/activate```
2. Установить зависимости ```pip install -r ./requirements.txt```
3. Создать ```.env``` файл и заполнить его (подставить свои параметры базы данных):
```dotenv
SECRET_KEY='django-insecure-)@0m!212vz+=p^jf1hu4th+4y)a(w%ieunf&^#8-l*db-b%60x'
ENV='dev'
DB_NAME='blog'
DB_HOST='localhost'
DB_PORT='5432'
DB_USER='postgres'
DB_PASSWORD='postgres'
```
4. Выполнить миграции ```python3 manage.py migrate```
5. Запустить приложение ```python3 manage.py runserver```

### Документация и взаимодействие через SWAGGER
http://localhost:8000/api/docs