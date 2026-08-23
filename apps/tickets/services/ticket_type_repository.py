from apps.tickets.repositories.ticket_type_repository import TicketTypeRepository


class TicketTypeService:

    def __init__(self):
        self.ticket_type_repository = TicketTypeRepository()

    def get_by_id(self, ticket_type_id):
        return self.ticket_type_repository.get_by_id(ticket_type_id)