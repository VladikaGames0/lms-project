import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_project.settings')
django.setup()

from materials.models import Course, Lesson  # noqa: E402
from users.models import User, Payment  # noqa: E402


def create_test_data():
    print("Создание тестовых данных...")

    superuser, created = User.objects.get_or_create(
        email='admin@example.com',
        defaults={'first_name': 'Admin', 'last_name': 'User', 'is_staff': True, 'is_superuser': True}
    )
    if created:
        superuser.set_password('admin123')
        superuser.save()
        print("Создан суперпользователь: admin@example.com")

    user, created = User.objects.get_or_create(
        email='student@example.com',
        defaults={'first_name': 'Student', 'last_name': 'User', 'phone': '+7 (999) 123-45-67', 'city': 'Москва'}
    )
    if created:
        user.set_password('student123')
        user.save()
        print("Создан пользователь: student@example.com")

    course1, _ = Course.objects.get_or_create(
        title='Python для начинающих',
        defaults={'description': 'Базовый курс', 'owner': user}
    )
    print(f"Курс: {course1.title}, владелец: {course1.owner}")

    course2, _ = Course.objects.get_or_create(
        title='Django для профессионалов',
        defaults={'description': 'Продвинутый курс', 'owner': user}
    )
    print(f"Курс: {course2.title}, владелец: {course2.owner}")

    lesson1, _ = Lesson.objects.get_or_create(
        title='Введение в Python',
        course=course1,
        defaults={'description': 'Первый урок', 'video_link': 'https://youtu.be/example1', 'owner': user}
    )
    print(f"Урок: {lesson1.title}, владелец: {lesson1.owner}")

    lesson2, _ = Lesson.objects.get_or_create(
        title='Переменные и типы данных',
        course=course1,
        defaults={'description': 'Второй урок', 'video_link': 'https://youtu.be/example2', 'owner': user}
    )
    print(f"Урок: {lesson2.title}, владелец: {lesson2.owner}")

    lesson3, _ = Lesson.objects.get_or_create(
        title='Введение в DRF',
        course=course2,
        defaults={'description': 'Первый урок DRF', 'video_link': 'https://youtu.be/example3', 'owner': user}
    )
    print(f"Урок: {lesson3.title}, владелец: {lesson3.owner}")

    Payment.objects.get_or_create(
        user=user, course=course1, defaults={'amount': 4990.00, 'payment_method': 'transfer'}
    )
    Payment.objects.get_or_create(
        user=user, lesson=lesson1, defaults={'amount': 1990.00, 'payment_method': 'cash'}
    )
    Payment.objects.get_or_create(
        user=user, course=course2, defaults={'amount': 7990.00, 'payment_method': 'transfer'}
    )
    print("Платежи созданы.")


if __name__ == "__main__":
    create_test_data()
