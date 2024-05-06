from rest_framework import serializers
from materials.models import Course, Lesson, CourseSubscription
from materials.validators import validate_video_url


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели урока (Lesson).
    Автоматически сериализует все поля модели.
    """
    video_url = serializers.URLField(validators=[validate_video_url])

    class Meta:
        model = Lesson
        fields = '__all__'  # Экспортирует все поля модели
        read_only_fields = ['owner']


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели курса (Course).
    Автоматически сериализует все поля модели.
    """

    class Meta:
        model = Course
        fields = '__all__'  # Экспортирует все поля модели
        read_only_fields = ['owner']


class CourseDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для подробного представления курса (Course).
    Включает количество уроков и подробную информацию о каждом уроке.
    Атрибуты:
        is_subscribed (int): Поле для подсчета количества уроков в курсе.
        lessons (LessonSerializer): Сериализатор для уроков, связанных с курсом.
    """
    is_subscribed = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)  # Добавляем сериализатор уроков

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'lessons',
                  'is_subscribed']  # Добавляем поле 'lessons' в fields

    def get_lessons_count(self, obj):
        """
        Возвращает количество уроков, связанных с курсом.
        Args:
            obj (Course): Экземпляр модели курса, для которого подсчитывается количество уроков.
        Returns:
            int: Количество уроков, связанных с курсом.
        """
        return obj.lessons.all().count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return CourseSubscription.objects.filter(user=user, course=obj).exists()
        return False


class CourseSubscriptionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели подписки на курс.

    Атрибуты:
        model (CourseSubscription): Модель подписки на курс.
        fields (list): Поля модели, которые будут сериализованы.
    """
    class Meta:
        """
        Метакласс, определяющий метаданные для сериализатора.

        Атрибуты:
            model (CourseSubscription): Модель, которая будет использоваться для сериализации.
            fields (list): Поля модели, которые будут сериализованы.
        """
        model = CourseSubscription
        fields = ['id', 'user', 'course']
