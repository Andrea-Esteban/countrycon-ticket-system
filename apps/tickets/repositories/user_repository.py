from apps.tickets.models import User


class UserRepository:

    def get_all(self):
        return User.objects.select_related("perfil").order_by("id")

    def get_by_id(self, user_id):
        return (
            User.objects
            .select_related("perfil")
            .filter(id=user_id)
            .first()
        )

    def get_by_username(self, username):
        return User.objects.filter(
            username=username
        ).first()

    def create(self, **data):
        return User.objects.create(**data)

    def save(self, user):
        user.save()

        return user