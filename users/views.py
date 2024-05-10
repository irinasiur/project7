import stripe
from django.http import HttpResponse
from rest_framework import generics, status

from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Payment, User
from .serializers import PaymentSerializer, UserSerializer
from .filters import PaymentFilter
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .services.stripe_service import create_stripe_product, create_stripe_price, create_checkout_session
import logging

logger = logging.getLogger(__name__)

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

    def create(self, request, *args, **kwargs):
        logger.debug("Request data: %s", request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Попытка сохранить объект платежа и создать соответствующие объекты в Stripe
        try:
            payment = serializer.save()  # Сохраняем объект платежа в базу данных

            # Создаем продукт и цену в Stripe
            product_id = create_stripe_product("Course Payment", f"Payment for course: {payment.paid_course.name}")
            price_id = create_stripe_price(payment.amount, 'usd', product_id)

            # Создаем сессию оплаты в Stripe
            success_url = 'http://your-domain.com/payment-success'
            cancel_url = 'http://your-domain.com/payment-cancel'
            session_url = create_checkout_session(price_id, success_url, cancel_url)

            # Сохраняем URL сессии в объекте платежа для доступа пользователя
            payment.stripe_session_url = session_url
            payment.save()

            # Возвращаем URL сессии как часть ответа API
            headers = self.get_success_headers(serializer.data)
            return Response({'url': payment.stripe_session_url}, status=status.HTTP_201_CREATED, headers=headers)

        except stripe.error.StripeError as e:
            # В случае ошибок Stripe возвращаем ошибку сервера
            return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            # В случае других ошибок возвращаем общую серверную ошибку
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def perform_create(self, serializer):
    #     """
    #     Переопределение метода создания платежа для интеграции с Stripe.
    #     """
    #     payment = serializer.save()  # Сохраняем объект платежа в базу данных
    #
    #     # Создаем продукт и цену в Stripe
    #     product_id = create_stripe_product("Course Payment", "Payment for course: {}".format(payment.paid_course.name))
    #     price_id = create_stripe_price(payment.amount, 'usd', product_id)
    #
    #     # Создаем сессию оплаты в Stripe
    #     success_url = 'http://your-domain.com/payment-success'
    #     cancel_url = 'http://your-domain.com/payment-cancel'
    #     session_url = create_checkout_session(price_id, success_url, cancel_url)
    #
    #     # Сохраняем URL сессии в объекте платежа для доступа пользователя
    #     payment.stripe_session_url = session_url
    #     payment.save()
    #     # Возвращаем URL сессии как часть ответа API
    #     return Response({'url': payment.stripe_session_url}, status=201)


class CreatePaymentSession(APIView):
    def post(self, request, *args, **kwargs):
        price_id = request.data.get('price_id')
        # product_id = request.data.get('product_id')
        amount = request.data.get('amount')

        success_url = 'http://localhost:8000/payment-success'
        cancel_url = 'http://localhost:8000/payment-cancel'
        session_url = create_checkout_session(price_id, success_url, cancel_url)
        # session_url = create_checkout_session(product_id, success_url, cancel_url)

        return Response({"url": session_url}, status=status.HTTP_201_CREATED)

def payment_success(request):
    # Здесь можно добавить логику обработки успешного платежа, например, запись в базу данных
    return HttpResponse("Payment was successful. Thank you!")


def home(request):
    return HttpResponse("Welcome to My Django Project!")


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
