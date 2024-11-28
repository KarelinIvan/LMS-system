from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        """ Создание пользователя, курса, урока"""

        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(title="Test Course")
        self.lesson = Lesson.objects.create(title='Test Lesson')
        self.client.force_authenticate(user=self.user)

    def test_lesson_create(self):
        """ Тестирование созданеия урока """
        url = reverse("lms:Lesson_create")
        data = {"title": "test", "description": "test"}
        response = self.client.post(url, data=data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get("title"), "test")

    def test_lessons_list(self):
        """ Тестирование отображения уроков """

        url = reverse('lms:Lesson_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_lesson_retrieve(self):
        """ Тестирование отображения урока """

        url = reverse('lms:Lesson_retrieve', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_update(self):
        """ Тестирование редактирования урока """

        url = reverse('lms:Lesson_update', args=(self.lesson.pk,))
        data = {"title": "Updated test", "description": "update test"}
        response = self.client.put(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Updated test")

    def test_lesson_destroy(self):
        """ Тестирование удаления урока """

        url = reverse('lms:Lesson_destroy', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)
