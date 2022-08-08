# Проект `api_yamdb` - api для сбора отзывов на произведения
## Описание

Проект `YaMDb` собирает отзывы пользователей на различные произведения.

### Алгоритм регистрации пользователей

Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами email и username на эндпоинт `/api/v1/auth/signup/`.

YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.

Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт` /api/v1/auth/token/`, в ответе на запрос ему приходит token (JWT-токен).

При желании пользователь отправляет PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполняет поля в своём профайле (описание полей — в документации).


### Подробное описание вы найдете в `xxx.xxx.xxx.xxx/redoc`

## Технологии в проекте

`Django REST framework, Docker, NGINX, Gunicorn, PostgreSQL`
## Инструкции по запуску

### Локально:

1. клонируйте скачайте себе репозиторий
2. установите виртуально окружение
3. активируйте `venv`, установите пакеты из `requirements.txt`
4. сделайте миграции и запустите проект командой `python api_yamdb/manage.py runserver`

### С помощью Docker:

Собрать образы Docker можно следующей командой:

1. > `docker-compose --project-directory ./infra up -d --build`
   
    в скрипте `docker-compose` прописано создание суперпользователя **admin** c почтой **admin@admin.ru**
    
    Внимание! пароль необходимо задать командой в ручном режиме:
    
    > `docker-compose --project-directory ./infra exec web python manage.py changepassword`

    После выполенения всех команд, при необходимости, можно загрузить фикстуры командой:
    > `docker-compose --project-directory ./infra exec web python manage.py loaddata fixtures.json`

## Автор

`Alexander Fedorovtsev` - https://t.me/fedorovtsev_alexander