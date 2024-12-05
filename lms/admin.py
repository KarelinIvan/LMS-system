from django.contrib import admin

from lms.models import Course, Lesson, Subscription


@admin.register(Course)
class UserCourse(admin.ModelAdmin):
    list_display = ("id", "title", "preview", "description", "owner")


@admin.register(Lesson)
class UserLesson(admin.ModelAdmin):
    list_display = ("id", "title", "course", "description", "preview", "link_to_video", "owner")


@admin.register(Subscription)
class UserSubscription(admin.ModelAdmin):
    list_display = ("id", "user", "course")
