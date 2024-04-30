from rest_framework import viewsets, generics

from materials.models import Course, Lesson
from materials.permissions import IsModeratorOrReadOnly, IsOwnerOrReadOnly
from materials.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    Представление для просмотра и редактирования экземпляров курсов.
    Автоматически предоставляет действия `list`, `create`, `retrieve`, `update` и `destroy`.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsModeratorOrReadOnly]

    def get_queryset(self):
        """
        Получает queryset курсов.
        Если пользователь аутентифицирован и не является модератором, то возвращает только курсы,
        принадлежащие этому пользователю, иначе возвращает все курсы.
        """
        if self.request.user.is_authenticated and not self.request.user.groups.filter(name='Moderators').exists():
            return Course.objects.filter(owner=self.request.user)
        return super().get_queryset()

    def get_serializer_class(self):
        """
        Возвращает класс сериализатора для курса. Использует CourseDetailSerializer
        для действия 'retrieve', чтобы предоставить подробный вид экземпляра курса,
        и CourseSerializer для всех других действий.
        """
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer


class LessonCreateAPIView(generics.CreateAPIView):
    """
    Представление для создания новых экземпляров уроков.
    """
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrReadOnly]


class LessonListAPIView(generics.ListAPIView):
    """
    Представление для просмотра списка всех экземпляров уроков.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrReadOnly]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Представление для получения подробного просмотра экземпляра урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrReadOnly]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Представление для обновления экземпляра урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrReadOnly]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Представление для удаления экземпляра урока.
    """
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
