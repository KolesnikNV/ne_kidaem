![Python](https://img.shields.io/badge/Python-blue)
![Django](https://img.shields.io/badge/Django-green)
![Django Rest Framework](https://img.shields.io/badge/Django%20Rest%20Framework-orange)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-blueviolet)
![Docker](https://img.shields.io/badge/Docker-blue)

# Тестовое задание для ne_kidaem

Этот проект реализует RESTful API для управления постами, подписками пользователей, лайками и прочитанными постами. Проект построен с использованием Django и Django REST framework.

### Основные функции:

- Аутентификация пользователей
- Создание, обновление и удаление постов
- Лайки и чтение постов
- Подписки пользователей на авторов
- Получение постов и новостной ленты пользователя


### Установка:
Клонируйте репозиторий проекта:

```git clone https://github.com/KolesnikNV/ne_kidaem.git```

```cd ne_kidaem```

Создайте файл .env в корневой директории проекта и добавьте следующие переменные окружения:

```SECRET_KEY = "YOUR_SECRET_KEY"```

```CELERY_BROKER_URL = "YOUR_CELERY_BROKER_URL"```

```ALLOWED_HOSTS = ["YOUR", "ALLOWED", "HOSTS"]```

```PG_NAME = PG_NAME```

```PG_USER = PG_USER```

```PG_PASSWORD = PG_PASSWORD```

```PG_HOST = PG_HOST```

```PG_PORT = PG_PORT```


Замените на соответствующие значения.

### Запуск проекта: 
```docker-compose up --build```

После выполения команды автоматически применятся миграции, будет создана база пользователей из 100 человек по 100 постов у каждого.

Для доступа к админ-панеде необходимо выполнить команды python manage.py createsuperuser

Доступ к API по адресу http://localhost:8000.

### API Endpoints
- POST /api/token/: Получение токена аутентификации.
- GET /api/posts/: Список всех постов или создание нового поста.
- GET /api/posts/{post_id}/: Получение, обновление или удаление конкретного поста.
- POST /api/posts/{post_id}/read/: Отметить пост как прочитанный.
- POST /api/posts/{post_id}/like/: Поставить лайк посту.
- GET /api/feed/: Список постов от подписанных авторов.
- GET /api/read/: Список постов, отмеченных как прочитанные пользователем.
- GET /api/like/: Список постов, которые понравились пользователю.
- GET /api/user/: Список пользователей.
- POST /api/user/{user_id}/subscribe/: Подписка на ленту пользователя.
- GET /api/user/{user_id}/posts/: Список постов конкретного пользователя.
