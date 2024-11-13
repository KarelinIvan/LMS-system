from django.urls import path
from rest_framework.routers import SimpleRouter

from lms.apps import LmsConfig
from lms.views import CourseViewSet, LessonCreateApiView, LessonListApiView, LessonRetrieveAPIView, LessonUpdateAPIView, LessonDestroyAPIView

app_name = LmsConfig.name

router = SimpleRouter()
router.register('', CourseViewSet)

urlpatterns = [
    path('lesson/', LessonListApiView.as_view()),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view()),
    path('lesson/create/', LessonCreateApiView.as_view()),
    path('lesson/<int:pk>/destroy/', LessonDestroyAPIView.as_view()),
    path('lesson/<int:pk>/update/', LessonUpdateAPIView.as_view())
]

urlpatterns += router.urls
