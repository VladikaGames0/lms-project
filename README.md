# LMS Project

Платформа онлайн-обучения на Django REST Framework.

## Стек

| Компонент | Технология |
|-----------|-----------|
| Backend | Django 5.1 + DRF |
| WSGI-сервер | Gunicorn |
| Reverse-proxy | Nginx |
| База данных | PostgreSQL 16 |
| Брокер задач | Redis 7 |
| Фоновые задачи | Celery + Celery Beat |
| Оркестрация | Docker Compose |
| CI/CD | GitHub Actions |

---

## Быстрый старт (локально)

```bash
# 1. Клонировать репозиторий
git clone https://github.com/YOUR_USERNAME/lms-project.git
cd lms-project

# 2. Создать .env из шаблона
cp .env.template .env
# Отредактировать .env — заполнить SECRET_KEY, пароли и т.д.

# 3. Запустить
docker compose up --build

# 4. Создать суперпользователя (в отдельном терминале)
docker compose exec web python manage.py createsuperuser
```

**Приложение:** http://localhost (через Nginx на порту 80)  
**Admin:** http://localhost/admin/  
**Swagger:** http://localhost/api/docs/

---

## Деплой на сервер

### Шаг 1. Подключитесь к серверу

```bash
ssh root@YOUR_SERVER_IP
```

### Шаг 2. Запустите скрипт настройки

```bash
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/lms-project/main/server_setup.sh
bash server_setup.sh https://github.com/YOUR_USERNAME/lms-project.git
```

Скрипт:
- Установит Docker и Git
- Создаст пользователя `deploy` (без root-прав)
- Настроит файрвол (открыты только порты 22 и 80)
- Сгенерирует SSH-ключ для GitHub Actions
- Склонирует репозиторий

### Шаг 3. Заполните .env на сервере

```bash
nano /home/deploy/lms-project/.env
```

Обязательно укажите:
- `SECRET_KEY` — длинная случайная строка
- `ALLOWED_HOSTS` — IP сервера или домен
- `DB_PASSWORD` — надёжный пароль
- `DB_HOST=db` и `REDIS_URL=redis://redis:6379/0`

### Шаг 4. Первый запуск на сервере

```bash
su - deploy
cd lms-project
docker compose up -d --build
docker compose exec web python manage.py createsuperuser
```

---

## GitHub Actions — настройка секретов

**Settings → Secrets and variables → Actions → New repository secret**

| Secret | Описание | Пример |
|--------|----------|--------|
| `SECRET_KEY` | Django secret key | `django-insecure-abc...` |
| `STRIPE_PUBLISHABLE_KEY` | Публичный ключ Stripe | `pk_test_...` |
| `STRIPE_SECRET_KEY` | Секретный ключ Stripe | `sk_test_...` |
| `SERVER_HOST` | IP сервера | `185.100.67.123` |
| `SERVER_USER` | Пользователь SSH | `deploy` |
| `SERVER_PORT` | Порт SSH | `22` |
| `SERVER_SSH_KEY` | Приватный SSH-ключ | `-----BEGIN OPENSSH...` |

---

## CI/CD пайплайн

```
git push origin main
        │
        ▼
┌───────────────┐
│  1. lint      │  flake8 — проверка стиля кода
└──────┬────────┘
       │ ✅
       ▼
┌───────────────┐
│  2. test      │  PostgreSQL + Redis в GitHub CI
│               │  manage.py test
└──────┬────────┘
       │ ✅
       ▼
┌───────────────┐
│  3. build     │  docker build — проверка сборки образа
└──────┬────────┘
       │ ✅ (только push в main)
       ▼
┌───────────────┐
│  4. deploy    │  SSH → git pull → docker compose up
└───────────────┘
```

> Деплой выполняется **только при push в `main`**. Pull requests проходят только lint + test.

---

## Управление на сервере

```bash
# Статус контейнеров
docker compose ps

# Логи приложения
docker compose logs -f web

# Перезапуск
docker compose restart web

# Остановить всё
docker compose down
```

---

## Переменные окружения

Все переменные описаны в `.env.template`. Реальный `.env` не коммитится в репозиторий (защищён `.gitignore`).
