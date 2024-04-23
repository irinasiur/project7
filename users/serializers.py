from rest_framework import serializers

from materials.serializers import CourseSerializer, LessonSerializer
from .models import Payment  # Убедитесь, что путь к моделям соответствует вашему расположению модели Payment.


class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Payment, предназначен для сериализации данных платежей.
    Включает дополнительные поля для отображения полного имени пользователя, деталей курса,
    деталей урока и локализованного отображения метода платежа.
    """
    user_full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    course_details = CourseSerializer(source='paid_course', read_only=True)
    lesson_details = LessonSerializer(source='paid_lesson', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)

    class Meta:
        """
        Мета-класс, указывающий модель данных и набор полей для сериализации. Все поля модели
        включены в сериализацию.
        """
        model = Payment
        fields = '__all__'  # Включите все поля модели
        extra_fields = ['user_full_name']
