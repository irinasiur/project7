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
        if request.user.is_moderator and request.method not in ['POST', 'DELETE']:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        """
        Определяет, имеет ли пользователь доступ к отдельным объектам.
        Все безопасные методы доступны всем пользователям.
        Действия, изменяющие данные (кроме создания и удаления), разрешены для модераторов.
        """
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user or (request.user.is_moderator and request.method not in ['POST', 'DELETE'])


class UserCanCreateButNotModerator(BasePermission):
    """
    Позволяет создавать объекты только обычным пользователям.
    Модераторы могут читать и изменять объекты, но не могут создавать и удалять их.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.method == "POST":
            return request.user.is_authenticated and not request.user.is_moderator
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.method == "POST":
            return request.user.is_authenticated and not request.user.is_moderator
        return obj.owner == request.user or (request.user.is_moderator and request.method not in ['POST', 'DELETE'])
