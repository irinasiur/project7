from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from materials.models import Course, Lesson
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

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [UserCanCreateButNotModerator]
        else:
            permission_classes = [IsModeratorOrReadOnly]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # Этот метод вызывается только если разрешения проходят проверку, так что безопасно сохранять
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_moderator:
                return Course.objects.all()
            return Course.objects.filter(owner=self.request.user)
        return Course.objects.none()

    def get_serializer_class(self):
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

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_moderator:
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
            if self.request.user.is_moderator:
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
            if self.request.user.is_moderator:
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
            if self.request.user.is_moderator:
                # Модераторы не могут удалять уроки
                return Lesson.objects.none()
            return Lesson.objects.filter(owner=self.request.user)