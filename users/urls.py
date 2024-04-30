from django.urls import path

from .apps import UsersConfig
from .views import PaymentListAPIView, PaymentCreateAPIView, UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = UsersConfig.name

urlpatterns = [
    # URL для получения списка всех платежей. Этот URL используется для просмотра списка платежей.
    path('payments/', PaymentListAPIView.as_view(), name='payment-list'),
    # URL для получения истории платежей. Предполагается использование того же представления, что и для списка платежей,
    # что может подразумевать, например, фильтрацию по дате или статусу в самом представлении.
    path('payments/history/', PaymentListAPIView.as_view(), name='payment-history'),
    # URL для создания нового платежа. Этот маршрут обращается к представлению, которое обрабатывает создание нового
    # платежа.
    path('payments/create/', PaymentCreateAPIView.as_view(), name='payment-create'),
    # URL для регистрации новых пользователей. Этот URL используется для обработки POST запросов
    # и создания новых пользователей.
    path('register/', UserViewSet.as_view({'post': 'create'}), name='register'),
    # URL для получения JWT токена
    path('login/', TokenObtainPairView.as_view(), name='login'),
    # URL для обновления JWT токена
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
