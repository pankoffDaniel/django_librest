from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """Админ может делать всё."""

    def has_object_permission(self, request, view, obj) -> bool:
        return request.user.is_staff

    def has_permission(self, request, view) -> bool:
        return request.user.is_staff


class IsOwner(permissions.BasePermission):
    """Владелец может делать всё."""

    def has_object_permission(self, request, view, obj) -> bool:
        return request.user == obj.user

    def has_permission(self, request, view) -> bool:
        return request.user.is_authenticated


class ReadOnly(permissions.BasePermission):
    """Можно только смотреть."""

    def has_object_permission(self, request, view, obj) -> bool:
        return request.method in permissions.SAFE_METHODS

    def has_permission(self, request, view) -> bool:
        return request.method in permissions.SAFE_METHODS
