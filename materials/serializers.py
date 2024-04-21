from rest_framework import serializers
from materials.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели урока (Lesson).

    Автоматически сериализует все поля модели.
    """
    class Meta:
        model = Lesson
        fields = '__all__'  # Экспортирует все поля модели


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели курса (Course).

    Автоматически сериализует все поля модели.
    """
    class Meta:
        model = Course
        fields = '__all__'  # Экспортирует все поля модели


class CourseDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для подробного представления курса (Course).

    Включает количество уроков и подробную информацию о каждом уроке.

    Атрибуты:
        lessons_count (int): Поле для подсчета количества уроков в курсе.
        lessons (LessonSerializer): Сериализатор для уроков, связанных с курсом.
    """
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)  # Добавляем сериализатор уроков

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'lessons_count', 'lessons']  # Добавляем поле 'lessons' в fields

    def get_lessons_count(self, obj):
        """
        Возвращает количество уроков, связанных с курсом.

        Args:
            obj (Course): Экземпляр модели курса, для которого подсчитывается количество уроков.

        Returns:
            int: Количество уроков, связанных с курсом.
        """
        return obj.lessons.all().count()





