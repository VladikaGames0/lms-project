from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import Course, Lesson, Subscription

User = get_user_model()


class LessonCRUDTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass123')
        self.moderator = User.objects.create_user(email='moderator@example.com', password='modpass123')
        self.course = Course.objects.create(title='Тестовый курс', owner=self.user)
        self.lesson = Lesson.objects.create(title='Тестовый урок', video_link='https://www.youtube.com/watch?v=test', course=self.course, owner=self.user)
        moderator_group, _ = Group.objects.get_or_create(name='moderators')
        self.moderator.groups.add(moderator_group)

    def test_create_lesson_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/lessons/', {'title': 'Новый урок', 'video_link': 'https://www.youtube.com/watch?v=new', 'course': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_lesson_invalid_youtube_url(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/lessons/', {'title': 'Новый урок', 'video_link': 'https://rutube.ru/test', 'course': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_lesson_owner(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/lessons/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_lesson_moderator_forbidden(self):
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(f'/api/lessons/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass123')
        self.course = Course.objects.create(title='Тестовый курс', owner=self.user)

    def test_add_subscription(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/courses/subscribe/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_remove_subscription(self):
        Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/courses/subscribe/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.count(), 0)