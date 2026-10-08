from rest_framework.permissions import BasePermission


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsOwnerOrSuperuser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj.owner == request.user


class IsSuperuserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return request.user.is_authenticated
        return request.user.is_superuser
