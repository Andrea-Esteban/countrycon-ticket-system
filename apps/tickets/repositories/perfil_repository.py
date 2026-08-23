from apps.tickets.models import Perfil


class PerfilRepository:

    def get_all(self):
        return Perfil.objects.all().order_by("id")