from apps.tickets.models import User
from apps.tickets.repositories.user_repository import UserRepository


class UserService:

    def __init__(self):
        self.repository = UserRepository()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, user_id):
        return self.repository.get_by_id(user_id)

    def create(self, username, password, perfil, is_active=True):

        if self.repository.get_by_username(username):
            raise ValueError(
                "El nombre de usuario ya existe."
            )

        user = User(
            username=username,
            perfil=perfil,
            is_active=is_active,
        )

        user.set_password(password)

        return self.repository.save(user)

    def update(
        self,
        user,
        username=None,
        password=None,
        perfil=None,
        is_active=None,
    ):

        if username is not None:

            existing_user = (
                self.repository.get_by_username(username)
            )

            if (
                existing_user
                and existing_user.id != user.id
            ):
                raise ValueError(
                    "El nombre de usuario ya existe."
                )

            user.username = username

        if password:
            user.set_password(password)

        if perfil is not None:
            user.perfil = perfil

        if is_active is not None:
            user.is_active = is_active

        return self.repository.save(user)