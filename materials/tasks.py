from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from .models import Course, Lesson
from users.tasks import send_course_update_email


@shared_task
def send_course_update_notification(course_id, updated_at):
    """
    Отправка уведомлений подписчикам курса об обновлении
    Проверяет, что курс не обновлялся более 4 часов
    """
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return f"Course {course_id} not found"

    # Проверка: не было ли обновлений за последние 4 часа
    last_update = course.updated_at if hasattr(course, 'updated_at') else updated_at
    four_hours_ago = timezone.now() - timedelta(hours=4)

    if last_update and last_update > four_hours_ago:
        return f"Course {course_id} was updated less than 4 hours ago. Skipping notifications."

    # Получаем подписчиков
    subscribers = course.subscriptions.select_related('user').all()

    if not subscribers.exists():
        return f"No subscribers for course {course_id}"

    # Отправляем уведомления
    for subscription in subscribers:
        send_course_update_email.delay(
            user_email=subscription.user.email,
            course_title=course.title,
            course_id=course.id
        )

    return f"Sent notifications to {subscribers.count()} subscribers for course {course_id}"