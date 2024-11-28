from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import User


class CourseTestCase(APITestCase):
    def setUp(self):
        """ Создание пользователя, курса, урока"""

        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(title="Test Course")
        self.lesson = Lesson.objects.create(title='Test Lesson')
        self.client.force_authenticate(user=self.user)
        self.course.lesson_set.add(self.lesson)

    def test_course_create(self):
        """Тестирование созданеия курса"""
        url = reverse('lms:course-list')
        data = {"title": "test", "description": "test"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)
