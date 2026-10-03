from django.db.models import Count, Q
from django.shortcuts import render

from apps.tickets.decorators import perfil_requerido
from apps.tickets.models import Ticket  # ajusta la ruta a tu modelo


@perfil_requerido("ADMIN", "VALIDATOR")
def home_view(request):
    ctx = {}

    if request.user.perfil.nombre == "ADMIN":
        ctx["stats"] = Ticket.objects.filter(is_active=True).aggregate(
            total=Count("id"),
            paid=Count("id", filter=Q(is_paid=True)),
            unpaid=Count("id", filter=Q(is_paid=False)),
            used=Count("id", filter=Q(is_used=True)),
            pending_entry=Count("id", filter=Q(is_paid=True, is_used=False)),
        )

    return render(request, "home.html", ctx)