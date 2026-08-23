from django.shortcuts import render

from apps.tickets.decorators import perfil_requerido


@perfil_requerido(
    "ADMIN",
    "VALIDATOR"
)
def scanner_view(request):

    return render(
        request,
        "tickets/scanner.html"
    )