from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """
    Администраторы: права на создание произведений, категорий и жанров.
    Юзеры: права чтение.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsModerOrAdminOrAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
        )

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class AdminAuthorModeratorOrReadOnly(permissions.BasePermission):
    """
    Администраторы, авторы, модераторы: права на запись.
    Юзеры: права на чтение.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )
