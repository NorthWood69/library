# Учебный проект Django Local Library

Готовый проект по результатам обучающего курса Mozilla Development Network (MDN) [MDN tutorial home page](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Tutorial_local_library_website).

## Общая информация

Данный проект создан в следующем окружении:

* Ubuntu 18.04.2 x86-64.
* Python 3.6.7.
* Django 2.2.1.
* PostgreSQL 10.8

## Запуск проекта

1. Установите [Python development environment](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/development_environment).
2. Установите PostgreSQL и создайте базу данных. Для создания базы данных выполните следующие шаги:

* Запустите psql от имени пользователя postgres. Например, <psql -U postgres>.
* Из коммандной строки psql выполните следующие комманды:
    ```
    CREATE DATABASE catalogdb;
    CREATE ROLE siteadmin WITH PASSWORD 'passwrd123';
    ALTER ROLE siteadmin SET client_encoding TO 'utf8';
    ALTER ROLE siteadmin SET default_transaction_isolation TO 'read committed';
    ALTER ROLE siteadmin SET timezone TO 'Europe/Moscow';
    GRANT ALL PRIVILEGES ON DATABASE catalogdb TO siteadmin;
    ALTER ROLE siteadmin CREATEDB;
    \q
    ```
* Скопируйте файлы проекта в удобную для Вас папку. Перейдите в папку с файлом manage.py и выполните следующие комманды:
    ```
    python3 manage.py makemigrations catalog
    python3 manage.py migrate
    python3 manage.py loaddata db.json
    python3 manage.py runserver
    ```
3. Откройте в браузере страницу `http://<IP_ADDRESS>:8000/admin/` для подключения к админке.
    ```
    Логин: siteadmin
    Пароль: passwrd123
    ```
4. Откройте в браузере страницу `http://<IP_ADDRESS>:8000` для подключения к основному сайту. Различные пользователи (можно посмотреть в админке) имеют разные права на сайт. Пароли у всех одинаковые.

5. Вы можете протестировать сайт заранее подготовленными тестами из папки <projectfolder>/catalog/tests. После выполнения теста не должно быть ни одной ошибки. Для теста перейдите в коневую папку проекта, где расположен файл manage.py и выполните команду:
    ```
    python3 manage.py test
    ```
