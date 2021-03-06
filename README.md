# Adverts

Adverts - сайт объявлений о продаже недвижимости, транспорта и разных вещей.
Adverts дает пользователям возможность создать учетную запись, опубликовать объявление. Объявление может быть привязано к категории или подкатегории.

## Стек технологий
- проект написан на Python с использованием веб-фреймворка Django.
- работа с изображениями - sorl-thumbnail, pillow
- система управления версиями - git
- база данных - SQLite

## Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:
```
    git clone https://github.com/Evgenia789/adverts
```
```
    cd adverts
```
Cоздать и активировать виртуальное окружение:
```
    python3 -m venv env
```
```
    source env/bin/activate
```
```
    python3 -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```
    pip install -r requirements.txt
```
Выполнить миграции:
```
    python3 manage.py migrate
```
Создайте суперпользователя:
```
    python3 manage.py createsuperuser
```
Запустить проект:
```
    python3 manage.py runserver
```
____
Ваш проект запустился на http://127.0.0.1:8000/  

## Планы по доработке
- добавить API  
- добавить тестирование  
