from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import User


class CourseTestCase(APITestCase):
    def setUp(self):
        """ Создание пользователя, курса, урока и добавление урока в курс """

        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(title="Test Course")
        self.lesson = Lesson.objects.create(title='Test Lesson')
        self.course.lesson_set.add(self.lesson)
        self.client.force_authenticate(user=self.user)

    def test_course_retrive(self):
        pass
