from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import Course, Lesson, Subscription

User = get_user_model()


class LessonCRUDTest(TestCase):
    """
    Тесты для CRUD операций с уроками
    """

    def setUp(self):
        """Подготовка тестовых данных"""
        self.client = APIClient()

        # Создаем пользователей
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

        self.moderator = User.objects.create_user(
            email='moderator@example.com',
            password='modpass123',
            first_name='Mod',
            last_name='User'
        )

        self.other_user = User.objects.create_user(
            email='other@example.com',
            password='otherpass123',
            first_name='Other',
            last_name='User'
        )

        # Создаем группу модераторов
        moderator_group, _ = Group.objects.get_or_create(name='moderators')
        self.moderator.groups.add(moderator_group)

        # Создаем курс
        self.course = Course.objects.create(
            title='Тестовый курс',
            description='Описание курса',
            owner=self.user
        )

        # Создаем урок
        self.lesson = Lesson.objects.create(
            title='Тестовый урок',
            description='Описание урока',
            video_link='https://www.youtube.com/watch?v=test',
            course=self.course,
            owner=self.user
        )

    def test_create_lesson_success(self):
        """Тест успешного создания урока"""
        self.client.force_authenticate(user=self.user)
        url = '/api/lessons/'
        data = {
            'title': 'Новый урок',
            'description': 'Описание',
            'video_link': 'https://www.youtube.com/watch?v=new',
            'course': self.course.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_lesson_invalid_youtube_url(self):
        """Тест создания урока с недопустимой ссылкой"""
        self.client.force_authenticate(user=self.user)
        url = '/api/lessons/'
        data = {
            'title': 'Новый урок',
            'description': 'Описание',
            'video_link': 'https://rutube.ru/video/test',
            'course': self.course.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('video_link', response.data)

    def test_update_lesson_owner(self):
        """Тест обновления урока владельцем"""
        self.client.force_authenticate(user=self.user)
        url = f'/api/lessons/{self.lesson.id}/'
        data = {'title': 'Обновленный урок'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Обновленный урок')

    def test_update_lesson_moderator(self):
        """Тест обновления урока модератором"""
        self.client.force_authenticate(user=self.moderator)
        url = f'/api/lessons/{self.lesson.id}/'
        data = {'title': 'Обновлено модератором'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Обновлено модератором')

    def test_delete_lesson_owner(self):
        """Тест удаления урока владельцем"""
        self.client.force_authenticate(user=self.user)
        url = f'/api/lessons/{self.lesson.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_delete_lesson_moderator_forbidden(self):
        """Тест: модератор не может удалить урок"""
        self.client.force_authenticate(user=self.moderator)
        url = f'/api/lessons/{self.lesson.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_lessons_pagination(self):
        """Тест пагинации уроков"""
        # Создаем 15 уроков
        for i in range(15):
            Lesson.objects.create(
                title=f'Урок {i}',
                description='Описание',
                video_link='https://www.youtube.com/watch?v=test',
                course=self.course,
                owner=self.user
            )

        self.client.force_authenticate(user=self.user)
        url = '/api/lessons/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertLessEqual(len(response.data['results']), 10)


class SubscriptionTest(TestCase):
    """
    Тесты для функционала подписки
    """

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )

        self.course = Course.objects.create(
            title='Тестовый курс',
            description='Описание курса',
            owner=self.user
        )

    def test_add_subscription(self):
        """Тест добавления подписки"""
        self.client.force_authenticate(user=self.user)
        url = '/api/courses/subscribe/'
        data = {'course_id': self.course.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_remove_subscription(self):
        """Тест удаления подписки"""
        Subscription.objects.create(user=self.user, course=self.course)

        self.client.force_authenticate(user=self.user)
        url = '/api/courses/subscribe/'
        data = {'course_id': self.course.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_subscription_without_course_id(self):
        """Тест подписки без указания course_id"""
        self.client.force_authenticate(user=self.user)
        url = '/api/courses/subscribe/'
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)


class CoursePaginationTest(TestCase):
    """
    Тесты пагинации курсов
    """

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )

        for i in range(12):
            Course.objects.create(
                title=f'Курс {i}',
                description='Описание',
                owner=self.user
            )

    def test_course_pagination(self):
        """Тест пагинации курсов"""
        self.client.force_authenticate(user=self.user)
        url = '/api/courses/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertLessEqual(len(response.data['results']), 5)
        self.assertIn('next', response.data)

    def test_course_pagination_with_page_size_param(self):
        """Тест пагинации с параметром page_size"""
        self.client.force_authenticate(user=self.user)
        url = '/api/courses/?page_size=3'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

    def test_course_pagination_max_page_size(self):
        """Тест ограничения максимального размера страницы"""
        self.client.force_authenticate(user=self.user)
        url = '/api/courses/?page_size=100'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(len(response.data['results']), 20)