from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsModeratorOrReadOnly(BasePermission):
    """
    Права доступа для модераторов или только чтение.
    Разрешает доступ к определенным действиям в зависимости от принадлежности пользователя к группе "Moderators".
    """
    def has_permission(self, request, view):
        """
        Проверка разрешения на уровне представления (для списка объектов).
        Разрешает доступ к безопасным методам и методам для аутентифицированных пользователей из группы "Moderators".
        """
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.groups.filter(name='Moderators').exists()

    def has_object_permission(self, request, view, obj):
        """
        Проверка разрешения на уровне объекта (для конкретного объекта).
        Разрешает доступ к объектам только для чтения для аутентифицированных пользователей из группы "Moderators".
        """
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.groups.filter(
            name='Moderators').exists() and request.method != 'DELETE'


class IsOwnerOrReadOnly(BasePermission):
    """
    Права доступа для владельца или только чтение.
    Разрешает доступ к объектам только для их владельца и разрешает только чтение для остальных пользователей.
    """
    def has_object_permission(self, request, view, obj):
        """
        Проверка разрешения на уровне объекта (для конкретного объекта).
        Разрешает доступ к объектам только для их владельца и разрешает только чтение для остальных пользователей.
        """
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user
