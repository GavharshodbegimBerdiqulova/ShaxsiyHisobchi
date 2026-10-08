from rest_framework.permissions import BasePermission


class IsSuperuser(BasePermission):
    # Faqat superadmin
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsOwnerOrSuperuser(BasePermission):
    # Oddiy foydalanuvchi faqat o'z yozuvini o'zgartira oladi, superadmin hammasini
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj.owner == request.user


class IsSuperuserOrReadOnly(BasePermission):
    # Valyutalarni hamma ko'ra oladi, o'zgartirishni faqat superadmin qiladi
    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return request.user.is_authenticated
        return request.user.is_superuser
