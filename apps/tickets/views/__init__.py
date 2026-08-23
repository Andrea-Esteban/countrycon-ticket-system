from django.shortcuts import render

from apps.tickets.decorators import perfil_requerido


@perfil_requerido("ADMIN")
def buyers_page(request):

    return render(
        request,
        "tickets/buyers.html"
    )