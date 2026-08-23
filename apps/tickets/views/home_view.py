from django.shortcuts import render

from apps.tickets.decorators import perfil_requerido


@perfil_requerido(
    "ADMIN",
    "VALIDADOR"
)
def home_view(request):

    return render(
        request,
        "home.html"
    )