# LMS Project

Платформа онлайн-обучения на Django REST Framework с поддержкой Celery, PostgreSQL и Redis.

## Стек технологий

- **Backend**: Django 5.1 + Django REST Framework
- **База данных**: PostgreSQL 16
- **Брокер задач**: Redis 7
- **Фоновые задачи**: Celery + Celery Beat
- **Аутентификация**: JWT (djangorestframework-simplejwt)
- **Платежи**: Stripe
- **Документация API**: drf-spectacular (OpenAPI/Swagger)

## Требования

- Docker и Docker Compose (версия 2.x+)

## Быстрый старт

### 1. Клонировать репозиторий

```bash
git clone <url-репозитория>
cd lms-project
```

### 2. Создать файл `.env`

Скопируйте пример и заполните своими значениями:

```bash
cp .env.example .env
```

Обязательно укажите в `.env`:
- `SECRET_KEY` — длинная случайная строка
- `DB_PASSWORD` — пароль для PostgreSQL
- `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD` — данные почты для уведомлений
- `STRIPE_PUBLISHABLE_KEY` / `STRIPE_SECRET_KEY` — ключи Stripe (можно оставить тестовые)

> ⚠️ Убедитесь, что в `.env` хосты указаны как имена сервисов Docker:
> - `DB_HOST=db`
> - `REDIS_URL=redis://redis:6379/0`

### 3. Запустить проект

```bash
docker compose up --build
```

При первом запуске Docker автоматически:
- Соберёт образ приложения
- Запустит PostgreSQL и Redis
- Применит миграции базы данных (`migrate`)
- Соберёт статику (`collectstatic`)
- Запустит Django-сервер, Celery worker и Celery Beat

### 4. Создать суперпользователя (опционально)

```bash
docker compose exec web python manage.py createsuperuser
```

### 5. Загрузить тестовые данные (опционально)

```bash
docker compose exec web python manage.py loaddata users/fixtures/groups.json
docker compose exec web python manage.py loaddata users/fixtures/payments.json
```

## Доступные URL

| Адрес | Описание |
|-------|----------|
| http://localhost:8000/ | Главная страница |
| http://localhost:8000/api/ | API корень |
| http://localhost:8000/api/schema/redoc/ | ReDoc документация |
| http://localhost:8000/admin/ | Django Admin |

## Управление контейнерами

```bash
# Запустить в фоновом режиме
docker compose up -d

# Остановить все контейнеры
docker compose down

# Остановить и удалить volumes (сбросить базу данных)
docker compose down -v

# Просмотр логов
docker compose logs -f

# Логи конкретного сервиса
docker compose logs -f web
docker compose logs -f celery

# Выполнить команду внутри контейнера
docker compose exec web python manage.py shell
```

## Структура сервисов

| Сервис | Образ | Доступ снаружи |
|--------|-------|----------------|
| `web` | Собственный (Dockerfile) | `localhost:8000` |
| `db` | postgres:16-alpine | Только внутри сети (expose) |
| `redis` | redis:7-alpine | Только внутри сети (expose) |
| `celery` | Собственный (Dockerfile) | Нет |
| `celery-beat` | Собственный (Dockerfile) | Нет |

## Переменные окружения

Все переменные описаны в файле `.env.example`. Реальный файл `.env` не коммитится в репозиторий.

| Переменная | Описание |
|-----------|----------|
| `SECRET_KEY` | Секретный ключ Django |
| `DEBUG` | Режим отладки (True/False) |
| `ALLOWED_HOSTS` | Разрешённые хосты (через запятую) |
| `DB_NAME` | Имя базы данных |
| `DB_USER` | Пользователь базы данных |
| `DB_PASSWORD` | Пароль базы данных |
| `DB_HOST` | Хост БД (в Docker: `db`) |
| `DB_PORT` | Порт БД (по умолчанию: `5432`) |
| `REDIS_URL` | URL Redis (в Docker: `redis://redis:6379/0`) |
| `EMAIL_HOST_USER` | Email для отправки уведомлений |
| `EMAIL_HOST_PASSWORD` | Пароль приложения Gmail |
| `STRIPE_PUBLISHABLE_KEY` | Публичный ключ Stripe |
| `STRIPE_SECRET_KEY` | Секретный ключ Stripe |
