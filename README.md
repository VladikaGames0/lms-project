# LMS Project

[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.17-red.svg)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)

LMS (Learning Management System) — это бэкенд-сервер для платформы онлайн-обучения, разработанный на Django REST Framework. Система позволяет создавать курсы и уроки, управлять пользователями и предоставляет REST API для интеграции с любым фронтендом.

## 📋 Функциональность

### 👤 Пользователи
- Регистрация и авторизация по email (вместо username)
- Профиль пользователя с полями: телефон, город, аватарка
- Админ-панель для управления пользователями

### 📚 Курсы
- Создание, чтение, обновление и удаление курсов (CRUD)
- Поля: название, превью (картинка), описание
- Автоматический подсчет количества уроков в курсе

### 📖 Уроки
- Создание, чтение, обновление и удаление уроков (CRUD)
- Поля: название, описание, превью, ссылка на видео
- Связь с курсом (один курс — много уроков)

## 🛠 Технологии

- **Python** 3.13
- **Django** 5.2
- **Django REST Framework** 3.17
- **SQLite** (для разработки)
- **Pillow** (работа с изображениями)
- **Poetry** (управление зависимостями)

## 🚀 Установка и запуск

### Требования
- Python 3.13 или выше
- Poetry

### Шаги по установке

1. **Клонирование репозитория**
```bash
git clone https://github.com/VladikaGames0/lms-project.git
cd lms-project