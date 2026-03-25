from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """
    Разрешает доступ только модераторам.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='moderators').exists()


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешает редактирование и удаление только владельцу объекта.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsOwner(permissions.BasePermission):
    """
    Разрешает доступ только владельцу объекта.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user