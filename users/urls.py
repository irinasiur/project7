from django.urls import path
from .views import PaymentListAPIView, PaymentCreateAPIView

urlpatterns = [
    # URL для получения списка всех платежей. Этот URL используется для просмотра списка платежей.
    path('payments/', PaymentListAPIView.as_view(), name='payment-list'),
    # URL для получения истории платежей. Предполагается использование того же представления что и для списка платежей,
    # что может подразумевать, например, фильтрацию по дате или статусу в самом представлении.
    path('payments/history/', PaymentListAPIView.as_view(), name='payment-history'),
    # URL для создания нового платежа. Этот маршрут обращается к представлению, которое обрабатывает создание нового
    # платежа.
    path('payments/create/', PaymentCreateAPIView.as_view(), name='payment-create'),
    ]