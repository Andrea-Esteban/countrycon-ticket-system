# apps/tickets/repositories/ticket_repository.py

from uuid import UUID
from apps.tickets.models import Ticket, Buyer
from django.utils import timezone
class TicketRepository:

    def get_by_code(self, code: str):
        return Ticket.objects.filter(
            code=code
        ).first()

    def get_by_id(self, ticket_id):
        return Ticket.objects.filter(
            id=ticket_id
        ).first()

    def get_by_qr(self, id_qr: UUID):
        return Ticket.objects.filter(
            id_qr=id_qr
        ).first()

    def get_by_qr_for_update(self, id_qr: UUID):
        return (
            Ticket.objects
            .select_for_update()
            .filter(id_qr=id_qr)
            .first()
        )

    def mark_as_used(self, ticket):
        ticket.is_used = True
        ticket.used_at = timezone.now()
        ticket.save(
            update_fields=[
                "is_used",
                "used_at",
                "updated_at",
            ]
        )

        return ticket

    def get_partner_info(self, partner_id):
        partner = Buyer.objects.filter(
            id=partner_id
        ).first()

        if not partner:
            return None

        return {
            "id": partner.id,
            "nombre": partner.nombre,
            "apellido_paterno": partner.apellido_paterno,
            "apellido_materno": partner.apellido_materno,
        }


    def create(
        self,
        buyer,
        ticket_type,
        gift_selections,
        created_by
    ):

        ticket = Ticket.objects.create(
            buyer=buyer,
            ticket_type=ticket_type,
            gift_selections=gift_selections,
            is_paid=False,
            created_by=created_by,
            updated_by=created_by,
            code="TEMP"
        )

        ticket.code = f"CT-{ticket.id:06d}"

        ticket.save(
            update_fields=[
                "code",
                "updated_at",
            ]
        )

        return ticket


    def update(self, ticket, **data):

        for field, value in data.items():
            setattr(ticket, field, value)

        ticket.save()

        return ticket
        
    def get_all(self):
        return Ticket.objects.select_related(
            "buyer",
            "ticket_type"
        ).filter(is_active=True).order_by("-id")

        