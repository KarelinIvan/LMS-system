from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.owner = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(title="Test_course", description="test", owner=self.owner)
        self.lesson = Lesson.objects.create(title="Test_lesson", description="test", owner=self.owner)
        self.non_owner_lesson = Lesson.objects.create(title="Test_lesson", description="test")
        self.client.force_authenticate(user=self.owner)

    # def test_lesson_update(self):
    #     """ Тестирование на обновление урока """
    #     url_lesson = reverse("lms:Lesson_update", args=(self.lesson.pk,))
    #     data = {"title": "New test lesson"}
    #     response_lesson = self.client.patch(url_lesson, data=data)
    #     self.assertEqual(response_lesson.status_code, status.HTTP_200_OK)
    #     data_json = response_lesson.json()
    #     self.assertEqual(data_json.get("title"), "New test lesson")
    #     # Проверка на не авторизованного пользователя
    #     url_lesson = reverse("lms:Lesson_update", args=(self.non_owner_lessom.pk,))
    #     data = {"title": "New test lesson"}
    #     response_lesson = self.client.patch(url_lesson, data=data)
    #     self.assertEqual(response_lesson.status_code, status.HTTP_403_FORBIDDEN)

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

        url = reverse("lms:Lesson_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_lesson_retrieve(self):
        """ Тестирование отображения урока """

        url = reverse("lms:Lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_update(self):
        """ Тестирование редактирования урока """

        url = reverse("lms:Lesson_update", args=(self.lesson.pk,))
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
        self.assertEqual(Lesson.objects.count(), 1)


class SubscriptionViewTest(APITestCase):

    def setUp(self):
        self.owner = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(title="Test_course", description="test", owner=self.owner)
        self.lesson = Lesson.objects.create(title="Test_lesson", description="test", owner=self.owner)
        self.non_owner_lesson = Lesson.objects.create(title="Test_lesson", description="test")
        self.client.force_authenticate(user=self.owner)
        self.subscription = Subscription.objects.create(course=self.course, user=self.owner)

    def test_add_subscription(self):
        """ Тест добавления подписки """
        url = reverse("lms:subscribe")
        data = {"course_id": self.course.pk, "user_id": self.owner.pk}
        response = self.client.post(url, data)
        print(response.json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.owner, course=self.course).exists())

    def test_remove_subscription(self):
        """ Тест удаления подписки """
        url = reverse("lms:subscribe")
        data = {"course_id": self.course.pk, "user_id": self.owner.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.owner, course=self.course).exists())

