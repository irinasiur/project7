from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsModeratorOrReadOnly(BasePermission):
    """
    Класс разрешений, который позволяет доступ только для чтения всем пользователям,
    но предоставляет расширенный доступ (без создания и удаления) пользователям, входящим в группу "Moderators".
    """

    def has_permission(self, request, view):
        """
        Определяет, имеет ли пользователь доступ к представлению на уровне коллекции.
        Все безопасные методы (только чтение) доступны всем пользователям.
        Действия, изменяющие данные (кроме создания и удаления), разрешены для модераторов.
        """
        if request.method in SAFE_METHODS:
            return True
        if request.user.groups.filter(name='Moderators').exists():
            return False  # Модераторы не могут создавать или удалять курсы и уроки
        return True

    def has_object_permission(self, request, view, obj):
        """
        Определяет, имеет ли пользователь доступ к отдельным объектам.
        Все безопасные методы доступны всем пользователям.
        Действия, изменяющие данные (кроме создания и удаления), разрешены для модераторов.
        """
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user or (
            request.user.groups.filter(name='Moderators').exists() and request.method not in ['POST', 'DELETE'])


class UserCanCreateButNotModerator(BasePermission):
    """
    Позволяет создавать объекты только обычным пользователям.
    Модераторы могут читать и изменять объекты, но не могут создавать и удалять их.
    """

    def has_permission(self, request, view):
        """
        Проверяет разрешение на выполнение операции над списком объектов.

        Args:
            request (HttpRequest): HTTP-запрос.
            view (APIView): Представление, в котором применяется разрешение.

        Returns:
            bool: True, если разрешение разрешает операцию, в противном случае False.
        """
        if request.method in SAFE_METHODS:
            return True
        if request.method == "POST":
            # Пользователь должен быть аутентифицирован и не должен быть в группе "Модераторы"
            return request.user.is_authenticated and not request.user.groups.filter(name='Moderators').exists()
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Проверяет разрешение на выполнение операции над конкретным объектом.

        Args:
            request (HttpRequest): HTTP-запрос.
            view (APIView): Представление, в котором применяется разрешение.
            obj: Объект, над которым проверяется разрешение.

        Returns:
            bool: True, если разрешение разрешает операцию, в противном случае False.
        """
        if request.method in SAFE_METHODS:
            return True
        if request.method == "POST":
            # Пользователь должен быть аутентифицирован и не должен быть в группе "Модераторы"
            return request.user.is_authenticated and not request.user.groups.filter(name='Moderators').exists()
        # Пользователь должен быть владельцем объекта или быть модератором и не выполнять POST или DELETE
        return obj.owner == request.user or (
            request.user.groups.filter(name='Moderators').exists() and request.method not in ['POST', 'DELETE'])
