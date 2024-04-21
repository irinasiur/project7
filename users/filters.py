from django_filters import rest_framework as filters
from .models import Payment


class PaymentFilter(filters.FilterSet):
    """
    Фильтр для сущности оплаты, позволяющий фильтровать записи по дате оплаты, методу оплаты,
    курсу и уроку. Поддерживает фильтрацию от минимальной до максимальной даты, выбор метода оплаты
    и фильтрацию по ID курса и урока.
    """
    min_date = filters.DateFilter(field_name="payment_date", lookup_expr='gte')
    max_date = filters.DateFilter(field_name="payment_date", lookup_expr='lte')
    payment_method = filters.ChoiceFilter(choices=(('cash', 'Cash'), ('transfer', 'Bank Transfer')))
    course = filters.NumberFilter(field_name='paid_course__id')
    lesson = filters.NumberFilter(field_name='paid_lesson__id')

    class Meta:
        """
        Мета-класс, определяющий модель, к которой применяется фильтр, и поля, по которым
        проводится фильтрация.
        """
        model = Payment
        fields = ['payment_date', 'payment_method', 'course', 'lesson']
