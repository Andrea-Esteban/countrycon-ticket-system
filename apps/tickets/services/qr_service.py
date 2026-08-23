from uuid import UUID
from django.db import transaction
from django.utils import timezone
from apps.tickets.repositories.ticket_repository import TicketRepository


class QRService:

    def __init__(self):
        self.ticket_repository = TicketRepository()

    @transaction.atomic
    def validate_qr(self, id_qr):

        ticket = self.ticket_repository.get_by_qr_for_update(id_qr)

        if not ticket:
            return {
                "valid": False,
                "message": "QR no encontrado",
                "status": "not_found",
                "error": "TICKET_NOT_FOUND",
            }

        ticket_data = {
            "id": ticket.id,
            "id_qr": str(ticket.id_qr),
            "code": ticket.code,
            "ticket_type": ticket.ticket_type.nombre,
        }

        if ticket.ticket_type.nombre == "VIP":

            regalos = ticket.ticket_type.regalos or {}
            gift_selections = ticket.gift_selections or {}

            llavero = regalos.get("llavero")

            if llavero:
                ticket_data["gift"] = {
                    "type": "llavero",
                    "quantity": llavero.get("cant", 0),
                    "selection": gift_selections.get("llavero"),
                }

        if ticket.buyer and ticket.buyer.partner:
            data_partner = self.ticket_repository.get_partner_info(ticket.buyer.partner.id)
            ticket_data["partner"] = data_partner
            
        if ticket.is_used:
            return {
                "valid": False,
                "message": "El ticket ya fue utilizado",
                "status": "already_used",
                "error": "TICKET_ALREADY_USED",
                "ticket": ticket_data,
                "used_at": timezone.localtime(ticket.used_at).isoformat(),
            }


        self.ticket_repository.mark_as_used(ticket)

        return {
            "valid": True,
            "message": "Ticket válido",
            "status": "valid",
            "ticket": ticket_data,
        }