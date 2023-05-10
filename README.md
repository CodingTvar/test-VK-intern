# Проект по VK friends 'API: интерфейс взаимодействия программ'
![Python](https://img.shields.io/badge/Python-3.9.10-blue)
![Django](https://img.shields.io/badge/Django-3.2.16-blue)
![Django_REST_framework](https://img.shields.io/badge/Django_REST_framework-3.12.4-blue)



## Описание проекта
Проект **VK friends** собирает **друзей** в один единый сервис.
**Пользователи сервиса** могут добавлять друг друга в **друзья**. Например, один пользователь с именем "User1" может отправить заявку на добавления в друзья другому существующему пользователю в сервисе друзей. А другой пользователь в то же время может отклонить, либо принять запрос в друзья. Каждый пользователь может зарегистрироваться в этом сервисе.
А также зарегистрированный пользователь может просматривать заявки в друзья или же отправленные заявки от него самого.

## Ресурсы

* Ресурс **auth**: регистрация.
* Ресурс **users**: пользователи.
* Ресурс **profiles**: профили пользователей, где отображаются их друзья.
* Ресурс **send_requests**: просмотр отправленных заявок в друзья.
* Ресурс **incoming_requests**: просмотр входящих заявок в друзья.
* Ресурс **accept_request**: принять завку в друзья.
* Ресурс **reject_request**: отклонить завку в друзья.
* Ресурс **status_friend**: просмотр статус дружбы с другим пользователем.
* Ресурс **delete_friend**: удалить пользователя из друзей.

## Пользовательские роли и права доступа

* **Аноним** — может просматривать друзей любого пользователя и профили.
* **Аутентифицированный пользователь** (user) — может читать всё, как и Аноним, может добавлять в друзья, удалять из друзей, принимать и отклонять заявки в друзья.



## Запуск проекта на локальном сервере
### Необходимое ПО

* python **3.9.10**
* pip

### Установка

> Для MacOs и Linux вместо python использовать python3

1. Клонировать репозиторий.
   ```
   $ git clone git@github.com:dkushlevich/api_yamdb.git
   ```
2. Cоздать и активировать виртуальное окружение:
    ```
      $ cd api_yamdb
      $ python -m venv venv
    ```
    Для Windows:
    ```
      $ source venv/Scripts/activate
    ```
    Для MacOs/Linux:
    ```
      $ source venv/bin/activate
    ```
3. Установить зависимости из файла requirements.txt:
    ```
    (venv) $ python -m pip install --upgrade pip
    (venv) $ pip install -r requirements.txt
    ```

4. Выполнить миграции:
    ```
    (venv) $ python manage.py migrate
    ```
После выполнения вышеперечисленных инструкций проект доступен по адресу http://127.0.0.1:8000/
> Подробная документация API доступна после запуска сервера по адресу http://127.0.0.1:8000/swagger/
> Или в отдельном файле **Документация для VK friends.md**

## Контакты

**Кирилл Чебодаев** 

[![Telegram Badge](https://img.shields.io/badge/-codingtvar-blue?style=social&logo=telegram&link=https://t.me/codingtvar)](https://t.me/codingtvar) [![Gmail Badge](https://img.shields.io/badge/-kchebodaevdu125@gmail.com-c14438?style=flat&logo=Gmail&logoColor=white&link=mailto:kchebodaevdu125@gmail.com)](mailto:kchebodaevdu125@gmail.com)
