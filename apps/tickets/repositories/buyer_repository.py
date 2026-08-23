from apps.tickets.models import Buyer


class BuyerRepository:

    def get_by_id(self, buyer_id):
        return Buyer.objects.filter(
            id=buyer_id
        ).first()

    def get_by_dni(self, dni):
        return Buyer.objects.filter(
            dni=dni
        ).first()

    def get_all(self):
        return Buyer.objects.all()

    def create(self, **data):
        return Buyer.objects.create(**data)

    def update(self, buyer, **data):

        for field, value in data.items():
            setattr(buyer, field, value)

        buyer.save()

        return buyer