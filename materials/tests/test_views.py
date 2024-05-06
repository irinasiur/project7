import uuid

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APITestCase
from rest_framework import status
from materials.models import Course, Lesson

User = get_user_model()


class LessonCRUDTests(APITestCase):
    """
    Тесты для CRUD-операций с уроками.
    """
    def setUp(self):
        """
        Подготовка данных для тестов.
        """
        # Создание пользователей с уникальным email
        unique_suffix_user = uuid.uuid4()  # Генерируем уникальный суффикс
        unique_suffix_mod = uuid.uuid4()  # Генерируем уникальный суффикс для модератора
        self.user = User.objects.create_user(
            username='user',
            email=f'user_{unique_suffix_user}@example.com',  # Уникальный email
            password='password'
        )
        self.moderator = User.objects.create_user(
            username='moderator',
            email=f'moderator_{unique_suffix_mod}@example.com',  # Уникальный email
            password='password'
        )
        moderators_group = Group.objects.create(name='Moderators')
        self.moderator.groups.add(moderators_group)

        # Создание курса
        self.course = Course.objects.create(
            title='Python Basics',
            description='Learn Python from scratch',
            owner=self.user
        )

        # Создание урока
        self.lesson = Lesson.objects.create(
            title='Introduction to Python',
            description='Python basics',
            course=self.course,
            owner=self.user
        )

    def test_lesson_create(self):
        """
        Тест создания нового урока.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('materials:lesson-create')
        data = {
            'title': 'Variables in Python',
            'description': 'Understanding variables',
            'course': self.course.id,
            'video_url': 'https://www.youtube.com/watch?v=examplevideo'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)  # Проверка создания нового урока

    def test_lesson_read(self):
        """
        Тест чтения информации об уроке.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('materials:lesson-detail', kwargs={'pk': self.lesson.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Introduction to Python')

    def test_lesson_update(self):
        """
        Тест обновления информации об уроке.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('materials:lesson-update', kwargs={'pk': self.lesson.id})
        data = {'title': 'Updated Lesson Title'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated Lesson Title')

    def test_lesson_delete(self):
        """
        Тест удаления урока.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('materials:lesson-delete', kwargs={'pk': self.lesson.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class CourseSubscriptionTests(APITestCase):
    """
    Тесты для подписки и отписки пользователя от курса.
    """
    def setUp(self):
        """
        Подготовка данных для тестов.
        """
        self.user = User.objects.create_user(username='user', password='password')
        self.course = Course.objects.create(
            title='Python Basics',
            description='Learn Python from scratch',
            owner=self.user
        )

    def test_course_subscribe(self):
        """
        Тест подписки пользователя на курс.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('materials:course-subscribe', kwargs={'course_id': self.course.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_course_unsubscribe(self):
        """
        Тест отписки пользователя от курса.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('materials:course-subscribe', kwargs={'course_id': self.course.id})
        self.client.post(url)  # Подписка для последующей отписки
        url_unsub = reverse('materials:course-unsubscribe', kwargs={'course_id': self.course.id})
        response = self.client.delete(url_unsub)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
