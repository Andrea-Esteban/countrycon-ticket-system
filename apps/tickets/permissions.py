from rest_framework.permissions import BasePermission


class IsAdminOrValidador(BasePermission):

    message = "No tienes permisos para realizar esta acción."

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        if not request.user.is_active:
            return False

        if not request.user.perfil:
            return False

        return request.user.perfil.nombre in [
            "ADMIN",
            "VALIDADOR",
        ]

class IsAdmin(BasePermission):

    message = "No tienes permisos para administrar usuarios."

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.is_active
            and request.user.perfil
            and request.user.perfil.nombre == "ADMIN"
        )