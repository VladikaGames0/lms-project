from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from users.models import User


@shared_task
def send_course_update_email(user_email, course_title, course_id):
    """
    Асинхронная отправка письма об обновлении курса
    """
    subject = f'Обновление курса: {course_title}'
    message = f"""
    Здравствуйте!

    Курс "{course_title}" был обновлен.
    Перейдите по ссылке, чтобы посмотреть изменения:
    http://localhost:8000/api/courses/{course_id}/

    С уважением,
    Команда LMS Project
    """
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False,
    )
    return f"Email sent to {user_email} about course {course_title}"


@shared_task
def deactivate_inactive_users():
    """
    Блокировка пользователей, которые не заходили более месяца
    """
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(
        last_login__lt=one_month_ago,
        is_active=True,
        is_superuser=False  # Не блокируем суперпользователей
    )

    count = inactive_users.count()
    inactive_users.update(is_active=False)

    return f"Deactivated {count} inactive users (last login before {one_month_ago})"
