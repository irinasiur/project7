from rest_framework import viewsets, generics

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    Представление для просмотра и редактирования экземпляров курсов.
    Автоматически предоставляет действия `list`, `create`, `retrieve`, `update` и `destroy`.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

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


class LessonListAPIView(generics.ListAPIView):
    """
    Представление для просмотра списка всех экземпляров уроков.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Представление для получения подробного просмотра экземпляра урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Представление для обновления экземпляра урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Представление для удаления экземпляра урока.
    """
    queryset = Lesson.objects.all()
