from django.shortcuts import render

from apps.tickets.decorators import perfil_requerido


@perfil_requerido("ADMIN")
def users_page(request):

    return render(
        request,
        "users.html"
    )