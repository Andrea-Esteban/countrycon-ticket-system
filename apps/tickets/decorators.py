from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseForbidden


def perfil_requerido(*perfiles):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect_to_login(
                    request.get_full_path()
                )

            if not request.user.perfil:
                return HttpResponseForbidden(
                    "Tu usuario no tiene un perfil asignado."
                )

            if request.user.perfil.nombre not in perfiles:
                return HttpResponseForbidden(
                    "No tienes permisos para acceder a esta sección."
                )

            return view_func(
                request,
                *args,
                **kwargs
            )

        return wrapper

    return decorator