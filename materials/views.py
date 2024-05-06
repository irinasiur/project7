from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson, CourseSubscription
from materials.paginators import StandardResultsSetPagination
from materials.permissions import IsModeratorOrReadOnly, UserCanCreateButNotModerator
from materials.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    Представление для просмотра и редактирования курсов.
    Ограничивает доступ, разрешая только модераторам видеть и редактировать все курсы,
    и пользователи могут видеть только свои курсы.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        """
        Получение списка разрешений, определяющих, какие действия могут быть выполнены.
        Для создания нового курса доступно только пользователям, не являющимся модераторами.
        Для просмотра, обновления и удаления доступно только модераторам.
        Возвращает:
        - List[Permission]: Список разрешений для текущего действия.
        """
        if self.action == 'create':
            permission_classes = [UserCanCreateButNotModerator]
        else:
            permission_classes = [IsModeratorOrReadOnly]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """
        Выполняет действия после успешного создания курса.
        Устанавливает владельца курса, равного текущему пользователю.
        Параметры:
        - serializer (CourseSerializer): Сериализатор, используемый для создания курса.
        """
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Получение набора данных курсов в зависимости от пользователя.
        Если пользователь аутентифицирован, модераторы могут видеть все курсы,
        в то время как обычные пользователи видят только свои курсы.
        Возвращает:
        - QuerySet: Набор данных курсов, соответствующий правам доступа текущего пользователя.
        """
        if self.request.user.is_authenticated:
            if self.request.user.groups.filter(name='Moderators').exists():
                return Course.objects.all()
            return Course.objects.filter(owner=self.request.user)
        return Course.objects.none()

    def get_serializer_class(self):
        """
        Получение класса сериализатора для текущего действия.
        Для действия 'retrieve' используется детальный сериализатор,
        для всех остальных действий используется обычный сериализатор.
        Возвращает:
        - Serializer: Класс сериализатора для текущего действия.
        """
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer


class LessonCreateAPIView(generics.CreateAPIView):
    """
    API представление для создания новых уроков.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [UserCanCreateButNotModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    """
    Представление для просмотра списка уроков.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.groups.filter(name='Moderators').exists():
                return Lesson.objects.all()
            return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Представление для детального просмотра урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModeratorOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.groups.filter(name='Moderators').exists():
                return Lesson.objects.all()
            return Lesson.objects.filter(owner=self.request.user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Представление для обновления урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModeratorOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.groups.filter(name='Moderators').exists():
                return Lesson.objects.all()
            return Lesson.objects.filter(owner=self.request.user)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Представление для удаления урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModeratorOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.groups.filter(name='Moderators').exists():
                return Lesson.objects.none()  # Модераторы не могут удалять уроки
            return Lesson.objects.filter(owner=self.request.user)


class CourseSubscriptionAPIView(APIView):
    """
    API-точка для работы с подписками на курсы.

    Поддерживаемые HTTP-методы:
    - POST: Подписаться на курс
    - DELETE: Отписаться от курса
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        """
        Подписаться на курс.

        Параметры:
        - course_id (int): ID курса, на который нужно подписаться.

        Возвращает:
        - Response: Сообщение о успешной подписке с HTTP-статусом 201,
                    или сообщение о том, что уже подписаны с HTTP-статусом 200,
                    или сообщение об ошибке с HTTP-статусом 404, если курс не найден.
        """
        course = Course.objects.filter(id=course_id).first()
        if not course:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        subscription, created = CourseSubscription.objects.get_or_create(user=request.user, course=course)
        if created:
            return Response({"message": "Subscribed successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Already subscribed"}, status=status.HTTP_200_OK)

    def delete(self, request, course_id):
        """
        Отписаться от курса.

        Параметры:
        - course_id (int): ID курса, с которого нужно отписаться.

        Возвращает:
        - Response: Сообщение об успешной отписке с HTTP-статусом 204,
                    или сообщение об ошибке с HTTP-статусом 404, если подписка не найдена.
        """
        subscription = CourseSubscription.objects.filter(user=request.user, course_id=course_id).first()
        if subscription:
            subscription.delete()
            return Response({"message": "Unsubscribed successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Subscription not found"}, status=status.HTTP_404_NOT_FOUND)
