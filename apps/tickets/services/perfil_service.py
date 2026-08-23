from apps.tickets.repositories.perfil_repository import PerfilRepository


class PerfilService:

    def __init__(self):
        self.repository = PerfilRepository()

    def get_all(self):
        return self.repository.get_all()