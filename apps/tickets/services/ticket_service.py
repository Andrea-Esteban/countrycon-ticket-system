from django.db import transaction

from apps.tickets.repositories.ticket_repository import TicketRepository
from apps.tickets.repositories.buyer_repository import BuyerRepository
from apps.tickets.repositories.ticket_type_repository import TicketTypeRepository
from apps.tickets.services.ticket_email_service import TicketEmailService


class TicketService:

    def __init__(self):

        self.ticket_repository = TicketRepository()

        self.buyer_repository = BuyerRepository()

        self.ticket_type_repository = TicketTypeRepository()

    @transaction.atomic
    def create_ticket(
        self,
        buyer_id,
        ticket_type_id,
        gift_selections,
        user
    ):

        buyer = self.buyer_repository.get_by_id(
            buyer_id
        )

        if not buyer:
            raise ValueError(
                "El comprador no existe."
            )

        ticket_type = self.ticket_type_repository.get_by_id(
            ticket_type_id
        )

        if not ticket_type:
            raise ValueError(
                "El tipo de ticket no existe."
            )

        gift_selections = gift_selections or {}

        self.validate_gift_selections(
            ticket_type,
            gift_selections
        )

        ticket = self.ticket_repository.create(
            buyer=buyer,
            ticket_type=ticket_type,
            gift_selections=gift_selections,
            created_by=user
        )

        return ticket
    def validate_gift_selections(
        self,
        ticket_type,
        gift_selections
    ):

        regalos = ticket_type.regalos or {}

        if not regalos:
            return

        gift_selections = gift_selections or {}

        for gift_type, gift_config in regalos.items():

            quantity = gift_config.get(
                "cant",
                0
            )

            available_options = gift_config.get(
                "list",
                []
            )

            selection = gift_selections.get(
                gift_type
            )

            if quantity > 0 and not selection:

                raise ValueError(
                    f"Debe seleccionar el regalo: {gift_type}."
                )

            if selection:

                if isinstance(selection, list):

                    for item in selection:

                        if item not in available_options:

                            raise ValueError(
                                f"La selección '{item}' "
                                f"no es válida para el regalo "
                                f"'{gift_type}'."
                            )

                else:

                    if selection not in available_options:

                        raise ValueError(
                            f"La selección '{selection}' "
                            f"no es válida para el regalo "
                            f"'{gift_type}'."
                        )

    def post(self, request):

        from apps.tickets.serializers import TicketSerializer
        from rest_framework.response import Response
        from rest_framework import status

        serializer = TicketSerializer(
            data=request.data,
            context={
                "request": request
            }
        )

        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            ticket = serializer.save()

        except ValueError as e:

            return Response(
                {
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            TicketSerializer(ticket).data,
            status=status.HTTP_201_CREATED
        )


    def mark_as_paid(self, ticket_id, user):

        ticket = self.ticket_repository.get_by_id(
            ticket_id
        )

        if not ticket:
            raise ValueError(
                "El ticket no existe."
            )

        if ticket.is_paid:
            return {
                "ticket": ticket,
                "already_paid": True,
            }

        ticket.is_paid = True
        ticket.updated_by = user

        ticket.save(
            update_fields=[
                "is_paid",
                "updated_by",
                "updated_at",
            ]
        )

        TicketEmailService().send_ticket_email(
            ticket
        )

        return {
            "ticket": ticket,
            "already_paid": False,
        }

    def get_all(self):
        return self.ticket_repository.get_all()


    def deactivate_ticket(self, ticket_id):

        ticket = self.ticket_repository.get_by_id(
            ticket_id
        )

        if not ticket:
            return None

        if ticket.is_used:
            raise ValueError(
                "No se puede desactivar un ticket que ya fue utilizado."
            )

        ticket.is_active = False

        ticket.save(
            update_fields=["is_active"]
        )

        return ticket

    def activate_ticket(self, ticket_id):

        ticket = self.ticket_repository.get_by_id(
            ticket_id
        )

        if not ticket:
            return None

        ticket.is_active = True

        ticket.save(
            update_fields=["is_active"]
        )

        return ticket

    def update_ticket(
        self,
        ticket_id,
        buyer_id=None,
        gift_selections=None,
        is_active=None,
    ):
        ticket = self.ticket_repository.get_by_id(ticket_id)
        
        if not ticket:
            return None

        # No permitir desactivar un ticket ya utilizado
        if is_active is False and ticket.is_used:
            raise ValueError(
                "No se puede desactivar un ticket que ya fue utilizado."
            )

        # Cambiar comprador
        if buyer_id is not None:

            buyer = self.buyer_repository.get_by_id(
                buyer_id
            )

            if not buyer:
                raise ValueError(
                    "El comprador no existe."
                )

            ticket.buyer = buyer

        # Cambiar regalo
        if gift_selections is not None:

            self.validate_gift_selections(
                ticket.ticket_type,
                gift_selections
            )

            ticket.gift_selections = gift_selections

        # Cambiar estado
        if is_active is not None:
            ticket.is_active = is_active

        ticket.save()

        return ticket

    def get_by_id(self, ticket_id):
        return self.ticket_repository.get_by_id(
            ticket_id
        )