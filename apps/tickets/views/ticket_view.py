from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.tickets.models import Ticket

from apps.tickets.serializers import TicketSerializer
from apps.tickets.services.ticket_service import TicketService



from apps.tickets.permissions import IsAdmin


class TicketView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin,
    ]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = TicketService()

    def get(self, request, ticket_id=None):

        service = TicketService()

        # detalle
        if ticket_id is not None:

            ticket = service.get_by_id(ticket_id)

            if not ticket:
                return Response(
                    {"message": "El ticket no existe."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            gift = None

            if ticket.ticket_type.nombre == "VIP":

                regalos = ticket.ticket_type.regalos or {}
                gift_selections = ticket.gift_selections or {}

                llavero = regalos.get("llavero")

                if llavero:
                    gift = {
                        "type": "llavero",
                        "quantity": llavero.get("cant", 0),
                        "selection": gift_selections.get("llavero"),
                    }

            data = {
                "id": ticket.id,
                "id_qr": str(ticket.id_qr),
                "code": ticket.code,
                "buyer": {
                    "id": ticket.buyer.id,
                    "nombre": ticket.buyer.nombre,
                    "apellido_paterno": ticket.buyer.apellido_paterno,
                    "apellido_materno": ticket.buyer.apellido_materno,
                },
                "ticket_type": ticket.ticket_type.nombre,
                "gift": gift,
                "is_paid": ticket.is_paid,
                "is_used": ticket.is_used,
                "is_active": ticket.is_active,
                "used_at": (
                    ticket.used_at.isoformat() if ticket.used_at else None
                ),
            }

            return Response(data, status=status.HTTP_200_OK)

        # listado
        tickets = service.get_all()

        data = []

        for ticket in tickets:
            gift = None

            if ticket.ticket_type.nombre == "VIP":

                regalos = ticket.ticket_type.regalos or {}
                gift_selections = ticket.gift_selections or {}

                llavero = regalos.get("llavero")

                if llavero:
                    gift = {
                        "type": "llavero",
                        "quantity": llavero.get("cant", 0),
                        "selection": gift_selections.get("llavero"),
                    }
            data.append({
                "id": ticket.id,
                "id_qr": str(ticket.id_qr),
                "code": ticket.code,
                "buyer": {
                    "id": ticket.buyer.id,
                    "nombre": ticket.buyer.nombre,
                    "apellido_paterno": ticket.buyer.apellido_paterno,
                    "apellido_materno": ticket.buyer.apellido_materno,
                },
                "ticket_type": ticket.ticket_type.nombre,
                "gift": gift,
                "is_paid": ticket.is_paid,
                "is_used": ticket.is_used,
                "is_active": ticket.is_active,
                "used_at": (
                    ticket.used_at.isoformat()
                    if ticket.used_at
                    else None
                ),
            })

        return Response(data, status=status.HTTP_200_OK)
    def post(self, request):

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

    # def patch(self, request, ticket_id):

    #     try:

    #         ticket = Ticket.objects.get(
    #             id=ticket_id
    #         )

    #     except Ticket.DoesNotExist:

    #         return Response(
    #             {
    #                 "message": "El ticket no existe."
    #             },
    #             status=status.HTTP_404_NOT_FOUND
    #         )

    #     serializer = TicketSerializer(
    #         ticket,
    #         data=request.data,
    #         partial=True,
    #         context={
    #             "request": request
    #         }
    #     )

    #     if not serializer.is_valid():

    #         return Response(
    #             serializer.errors,
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    #     try:

    #         ticket = serializer.save()

    #     except ValueError as e:

    #         return Response(
    #             {
    #                 "message": str(e)
    #             },
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    #     return Response(
    #         TicketSerializer(ticket).data,
    #         status=status.HTTP_200_OK
    #     )

    def patch(self, request, ticket_id):

        service = TicketService()

        ticket = service.ticket_repository.get_by_id(
            ticket_id
        )

        if not ticket:
            return Response(
                {
                    "message": "Ticket no encontrado",
                    "error": "TICKET_NOT_FOUND",
                },
                status=status.HTTP_404_NOT_FOUND
            )

        data = request.data
        try:

            # Marcar como pagado
            if data.get("is_paid") is True:

                result = service.mark_as_paid(
                    ticket_id=ticket_id,
                    user=request.user
                )

                return Response(
                    {
                        "message": (
                            "Ticket ya estaba pagado."
                            if result["already_paid"]
                            else "Ticket marcado como pagado correctamente."
                        ),
                        "ticket": TicketSerializer(
                            result["ticket"]
                        ).data
                    },
                    status=status.HTTP_200_OK
                )
            # Actualizar ticket
            ticket = self.service.update_ticket(
                ticket_id=ticket_id,
                buyer_id=data.get("buyer_id"),
                gift_selections=data.get("gift_selections"),
                is_active=data.get("is_active"),
            )

            if not ticket:
                return Response(
                    {
                        "message": "Ticket no encontrado",
                        "error": "TICKET_NOT_FOUND",
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

        except ValueError as e:

            return Response(
                {
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "message": "Ticket actualizado correctamente.",
                "ticket": TicketSerializer(ticket).data
            },
            status=status.HTTP_200_OK
        )