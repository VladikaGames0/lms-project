import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_project.settings')
django.setup()

from materials.models import Course, Lesson
from users.models import User, Payment


def create_test_data():
    print("=" * 60)
    print("Создание тестовых данных для LMS проекта")
    print("=" * 60)

    # Создаем суперпользователя
    superuser, created = User.objects.get_or_create(
        email='admin@example.com',
        defaults={
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        superuser.set_password('admin123')
        superuser.save()
        print("✓ Создан суперпользователь: admin@example.com (пароль: admin123)")
    else:
        print("✓ Суперпользователь уже существует: admin@example.com")

    # Создаем обычного пользователя
    user, created = User.objects.get_or_create(
        email='student@example.com',
        defaults={
            'first_name': 'Student',
            'last_name': 'User',
            'phone': '+7 (999) 123-45-67',
            'city': 'Москва'
        }
    )
    if created:
        user.set_password('student123')
        user.save()
        print("✓ Создан пользователь: student@example.com (пароль: student123)")
    else:
        print("✓ Пользователь уже существует: student@example.com")

    # Создаем курс 1
    course1, created = Course.objects.get_or_create(
        title='Python для начинающих',
        defaults={
            'description': 'Базовый курс по Python программированию. Изучите основы Python с нуля.'
        }
    )
    print(f"✓ {'Создан' if created else 'Найден'} курс: {course1.title} (ID: {course1.id})")

    # Создаем курс 2
    course2, created = Course.objects.get_or_create(
        title='Django для профессионалов',
        defaults={
            'description': 'Продвинутый курс по Django REST Framework. Создание API, авторизация, оптимизация.'
        }
    )
    print(f"✓ {'Создан' if created else 'Найден'} курс: {course2.title} (ID: {course2.id})")

    # Создаем уроки для курса 1
    lesson1, created = Lesson.objects.get_or_create(
        title='Введение в Python',
        course=course1,
        defaults={
            'description': 'Первый урок курса. Установка Python, настройка окружения, первая программа.',
            'video_link': 'https://www.youtube.com/watch?v=python-intro'
        }
    )
    print(f"✓ {'Создан' if created else 'Найден'} урок: {lesson1.title} (ID: {lesson1.id})")

    lesson2, created = Lesson.objects.get_or_create(
        title='Переменные и типы данных',
        course=course1,
        defaults={
            'description': 'Второй урок. Изучение переменных, строк, чисел, списков и словарей.',
            'video_link': 'https://www.youtube.com/watch?v=python-variables'
        }
    )
    print(f"✓ {'Создан' if created else 'Найден'} урок: {lesson2.title} (ID: {lesson2.id})")

    # Создаем урок для курса 2
    lesson3, created = Lesson.objects.get_or_create(
        title='Введение в DRF',
        course=course2,
        defaults={
            'description': 'Первый урок. Установка DRF, создание простого API.',
            'video_link': 'https://www.youtube.com/watch?v=drf-intro'
        }
    )
    print(f"✓ {'Создан' if created else 'Найден'} урок: {lesson3.title} (ID: {lesson3.id})")

    # Создаем платежи
    payments_data = [
        {
            'user': user,
            'course': course1,
            'lesson': None,
            'amount': 4990.00,
            'payment_method': 'transfer'
        },
        {
            'user': user,
            'course': None,
            'lesson': lesson1,
            'amount': 1990.00,
            'payment_method': 'cash'
        },
        {
            'user': user,
            'course': course2,
            'lesson': None,
            'amount': 7990.00,
            'payment_method': 'transfer'
        },
        {
            'user': superuser,
            'course': course1,
            'lesson': None,
            'amount': 4990.00,
            'payment_method': 'transfer'
        }
    ]

    for data in payments_data:
        # Проверяем, существует ли уже такой платеж
        existing_payment = Payment.objects.filter(
            user=data['user'],
            course=data['course'],
            lesson=data['lesson']
        ).first()

        if existing_payment:
            print(
                f"✓ Платеж уже существует: {data['user'].email} - {data['course'].title if data['course'] else data['lesson'].title} - {data['amount']} руб.")
        else:
            payment = Payment.objects.create(
                user=data['user'],
                course=data['course'],
                lesson=data['lesson'],
                amount=data['amount'],
                payment_method=data['payment_method']
            )
            paid_item = data['course'].title if data['course'] else data['lesson'].title
            print(
                f"✓ Создан платеж: {data['user'].email} - {paid_item} - {data['amount']} руб. ({data['payment_method']})")

    print("\n" + "=" * 60)
    print("СТАТИСТИКА:")
    print(f"  - Пользователей: {User.objects.count()}")
    print(f"  - Курсов: {Course.objects.count()}")
    print(f"  - Уроков: {Lesson.objects.count()}")
    print(f"  - Платежей: {Payment.objects.count()}")
    print("=" * 60)
    print("\n✅ Все тестовые данные успешно созданы!")
    print("\n📌 Для входа в админку:")
    print("   http://localhost:8000/admin/")
    print("   Логин: admin@example.com")
    print("   Пароль: admin123")
    print("\n📌 Для входа как студент:")
    print("   Логин: student@example.com")
    print("   Пароль: student123")
    print("\n📌 API Endpoints для проверки:")
    print("   GET  http://localhost:8000/api/courses/")
    print("   GET  http://localhost:8000/api/users/payments/")
    print("   GET  http://localhost:8000/api/users/profile/")
    print("\n📌 Фильтрация платежей:")
    print("   GET  http://localhost:8000/api/users/payments/?payment_method=transfer")
    print("   GET  http://localhost:8000/api/users/payments/?course=1")
    print("   GET  http://localhost:8000/api/users/payments/?ordering=payment_date")


if __name__ == "__main__":
    create_test_data()