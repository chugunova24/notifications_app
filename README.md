Микросервис уведомления пользователей
==============
***Содержание:***
- [Введение](#Introduction)
- [Стек технологий](#Technology-stack)
- [Запуск контейнеров](#Run-container)
- [Тестирование API (пример с Postman)](#Testing-Api)


# Введение <a name="Introduction"></a>
notifications_app - это микросервис, представляющий из себя RestAPI сервер, который позволяет создавать запись уведомления в документе пользователя в MongoDB, отправлять email, а так же предоставлять листинг уведомлений из документа пользователя.

Для реализации были выбраны инструменты, описанные в пункте "Стек технологий" (ниже).
 - Flask отличный выбор для построения гибких веб-приложений. 
 - С помощью poetry удобно управлять версией языка в проекте, зависимостями, подключаемыми путями, скриптами тестирования/разработки, сборкой и публикацией билдов.
 - MongoDB это быстрая, удобная в маштабировании распределенная (способна работать на нескольких серверах) СУБД.
 - Redis в данном проекте используется как брокер сообщений.
 - Celery используется для создания и управления очередью задач. Интсрумент позволяет с легкостью маштабироваться. Это разумный выбор для проекта, в котором количество отложенных задач постоянно растет.
 - Docker использовался для контейнеризации инфраструктуры приложений. Инфраструктура определена в файле ./docker-compose.yaml, а сборка образа происходит через ./compose/flask/Dockerfile

# Стек технологий <a name="Technology-stack"></a>

- Веб-фреймворк - [Flask](https://flask.palletsprojects.com/en/2.2.x/)
- Инструмент для управления зависимостями в Python - [Poetry](https://python-poetry.org/)
- NoSQL (документоориентированная) БД - [MongoDB](http://mongoengine.org/)
- NoSQL (ключ-значение) БД - [Redis](https://redis.io/)
- Графический интерфейс к MongoDB - [MongoExpress](https://hub.docker.com/_/mongo-express)
- Графический интерфейс к Redis - [RedisInsight](https://hub.docker.com/r/redislabs/redisinsight)
- Платформа для контейнеризации - [Docker](https://www.docker.com/)


# Запуск контейнеров <a name="Run-container"></a>
Предполагается, что у Вас уже установлен Docker Engine.

1. <b>Склонируйте репозиторий на свой компьютер с помощью команды</b>:
   ```
   git clone https://github.com/chugunova24/notifications_app
   ```
2. <b>Зайдите в папку проекта</b>:
   ```
   cd notifications_app
   ```
3. <b>Замените значения переменных в файле ./.env</b>:

   Пример заполнения:
   ```
   # SMTP-server settings
   MAIL_SERVER='smtp.googlemail.com'
   MAIL_PORT=465
   MAIL_USE_SSL=True
   MAIL_USERNAME='test@gmail.com'
   MAIL_PASSWORD='your_secret_password'
   ```

4. <b>Выполните одну из следующих команд для сборки всех сервисов в зависимости от версии Docker</b>:

   ```
   docker-compose up -d 
   ```
   или:
   ```
   docker compose up -d
   ```

5. <b>После завершения установки Вы сможете пройти по следующим адресам</b>:
   * notifications_app:
        1)  http://0.0.0.0:5000/create
        2)  http://0.0.0.0:5000/list
        3)  http://0.0.0.0:5000/read
        4)  http://0.0.0.0:5000/register
   * MongoExpress - http://0.0.0.0:8081/
   * RedisInsight - http://0.0.0.0:8001/
   * Flower (Celery dashboard) - http://0.0.0.0:5555

# Доступ к RedisInsight и MongoExpress

RedisInsight:
* host: redis_aceplace
* port: 6379
* logic_name_db: 0
* name: redis-local
* username: default
* password: 123456

MongoExpress:
* login: admin
* password: pass

# Тестирование API (пример с Postman) <a name="Testing-Api"></a>

Предполагается, что у Вас уже установлена программа Postman.

1. <b>Создание уведомления "/create".
    Обратите внимание, сервер ожидает данные типа "application/json"</b>:
    ```
    POST http://0.0.0.0:5000/create
    ```
    Запрос клиента:
    ```
    {
        "user_id": "6549bd3c71be4dd518bf1ef8",
        "key": "new_post",
        "target_id": "6549bd3c71be4dd518bf1ef9",
        "data": {
            "some_key": "some_value"
        },
        "email": "test.testest@list.ru"
    }
    ```
    Ответ сервера:
    ```
    {
        "success": true
    }
    ```
    Документ пользователя в MongoDB (в формате bson):
    ```
    {
        _id: ObjectId('6549bd3c71be4dd518bf1ef8'),
        username: 'test4436',
        password: 'A123sew!sw',
        email: 'test.testest@list.ru',
        notifications: [
            {
                id: 1,
                timestamp: 1699377115,
                is_new: true,
                user_id: ObjectId('6549bd3c71be4dd518bf1ef8'),
                key: 'new_post',
                target_id: ObjectId('6549bd3c71be4dd518bf1ef9'),
                data: {
                    some_key: 'some_value'
                }
            }
        ]
    }
    ```
    Postman:
<p align="center">
<img src="https://github.com/chugunova24/notifications_app/blob/master/img_readme/create.png" style="width:60%;height:60%"/>
</p>

2. <b>Список уведомлений пользователя "/list"</b>
    ```
    GET http://0.0.0.0:5000/list?user_id=6549bd3c71be4dd518bf1ef8&limit=10&skip=0
    ```
    Ответ сервеера:
    ```
    {
        "success": true,
        "data": {
            "elements": 1,
            "new": 1,
            "request": {
                "user_id": "6549bd3c71be4dd518bf1ef8",
                "skip": 0,
                "limit": 10
            },
            "list": [
                {
                    "id": 1,
                    "timestamp": 1699377115,
                    "is_new": true,
                    "user_id": "6549bd3c71be4dd518bf1ef8",
                    "key": "new_post",
                    "target_id": "6549bd3c71be4dd518bf1ef9",
                    "data": {
                        "some_key": "some_value"
                    }
                }
            ]
        }
    }
    ```

    Postman:
<p align="center">
<img src="https://github.com/chugunova24/notifications_app/blob/master/img_readme/list.png" style="width:60%;height:60%"/>
</p>

    
    
3. <b>Пометить уведомление как прочитанное "/read".
    Сервер принимает данные как "multipart/form-data" (form-data):</b>
    ```
    POST http://0.0.0.0:5000/read
    ```
    
    Запрос клиента:
    ```
    {
        "user_id": "6549bd3c71be4dd518bf1ef8",
        "notification_id": "1"
    }
    ```
    Ответ сервера:
    ```
    {
        "success": true
    }
    ```
    Документ пользователя в MongoDB (в формате bson):
    ```
    {
        _id: ObjectId('6549bd3c71be4dd518bf1ef8'),
        username: 'test4436',
        password: 'A123sew!sw',
        email: 'test.testest@list.ru',
        notifications: [
            {
                id: 1,
                timestamp: 1699377115,
                is_new: false,
                user_id: ObjectId('6549bd3c71be4dd518bf1ef8'),
                key: 'new_post',
                target_id: ObjectId('6549bd3c71be4dd518bf1ef9'),
                data: {
                    some_key: 'some_value'
                }
            }
        ]
    }
    ```
    Postman:
<p align="center">
<img src="https://github.com/chugunova24/notifications_app/blob/master/img_readme/read.png" style="width:60%;height:60%"/>
</p>