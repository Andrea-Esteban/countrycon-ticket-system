from apps.tickets.models import TicketType


class TicketTypeRepository:

    def get_by_id(self, ticket_type_id):
        return TicketType.objects.filter(
            id=ticket_type_id
        ).first()

    def get_all(self):
        return TicketType.objects.all()