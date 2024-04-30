from rest_framework import generics

from django_filters import rest_framework as filters
# from rest_framework.generics import CreateAPIView

from .models import Payment, User
from .serializers import PaymentSerializer, UserSerializer
from .filters import PaymentFilter
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
# from typing import Type
# from django.contrib.auth import get_user_model


# User = get_user_model()


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


class UserViewSet(viewsets.ModelViewSet):
    """
     Представление для работы с пользователями.
     """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Определяет разрешения в зависимости от действия: для создания пользователей разрешено использование
        без авторизации (AllowAny), в остальных случаях требуется аутентификация (IsAuthenticated).
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Переопределение метода создания пользователя для установки пароля."""
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()
