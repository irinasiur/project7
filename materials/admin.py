from django.contrib import admin
from .models import Course, Lesson


# Регистрация модели Course в административной панели Django
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Административная конфигурация для модели курса.
    Определяет, какие поля отображать в списке курсов и добавляет функцию поиска по названию и описанию.
    """
    list_display = ['title', 'description', 'owner']  # Вы можете настроить, какие поля отображать в списке
    search_fields = ['title', 'description']  # Добавление поиска по названию и описанию


# Регистрация модели Lesson в административной панели Django
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """
    Административная конфигурация для модели урока.
    Определяет, какие поля отображать в списке уроков и добавляет функцию поиска по названию и описанию.
    """
    list_display = ['title', 'course', 'description', 'owner']  # Поля для отображения в списке уроков
    search_fields = ['title', 'description']  # Поля для поиска по названию и описанию
