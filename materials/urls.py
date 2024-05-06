from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, \
    LessonRetrieveAPIView, LessonUpdateAPIView, LessonDestroyAPIView, CourseSubscriptionAPIView

# Название приложения, используемое для обращения к URL внутри Django.
app_name = MaterialsConfig.name

# Создание маршрутизатора для ViewSet курсов.
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

# Определение шаблонов URL.
urlpatterns = [
    # path('', include(router.urls)),
    # URL для создания урока. Использует представление для создания одного урока.
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    # URL для получения списка уроков. Использует представление для списка уроков.
    path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    # URL для получения деталей урока по его ID. Использует представление для получения одного урока.
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-detail'),
    # URL для обновления урока. Использует представление для обновления урока по ID.
    path('lessons/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    # URL для удаления урока. Использует представление для удаления урока по ID.
    path('lessons/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),

    # Новыq URL для подписки и отписки от курсов.
    path('courses/<int:course_id>/subscribe/', CourseSubscriptionAPIView.as_view(),
         name='course-subscribe'),
    path('courses/<int:course_id>/unsubscribe/', CourseSubscriptionAPIView.as_view(), name='course-unsubscribe'),  # Добавлен URL для отписки
] + router.urls
