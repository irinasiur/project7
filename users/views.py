from rest_framework import generics

from django_filters import rest_framework as filters
from .models import Payment
from .serializers import PaymentSerializer
from .filters import PaymentFilter


class PaymentListAPIView(generics.ListAPIView):
    """
    Представление для получения списка всех платежей с возможностью фильтрации и сортировки.
    Использует PaymentSerializer для сериализации данных и PaymentFilter для фильтрации списка платежей.
    Сортировка реализована по дате платежа.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']
    ordering = ['payment_date']  # Сортировка по умолчанию

    def get_queryset(self):
        """
        Возвращает queryset всех платежей. Этот метод может быть модифицирован для
        реализации различной логики выборки в зависимости от статуса аутентификации пользователя.
        """
        return Payment.objects.all()


class PaymentCreateAPIView(generics.CreateAPIView):
    """
    Представление для создания нового платежа. Использует PaymentSerializer для валидации
    и сериализации входящих данных. Все экземпляры создаются с использованием данных, полученных
    из POST-запроса.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

# class PaymentListAPIView(generics.ListAPIView):
#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer
#     filter_backends = [filters.DjangoFilterBackend]
#     filterset_class = PaymentFilter
#     ordering_fields = ['payment_date']
#     ordering = ['payment_date']  # Сортировка по умолчанию
#
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_authenticated:
#             return Payment.objects.filter(user=user)
#         else:
#             # Вариант 1: Возвращаем пустой queryset, если пользователь не аутентифицирован
#             return Payment.objects.none()
#
