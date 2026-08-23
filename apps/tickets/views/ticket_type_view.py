from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.tickets.services.ticket_type_service import TicketTypeService

class TicketTypeListView(APIView):

    def get(self, request):

        service = TicketTypeService()

        ticket_types = service.get_all()

        data = []

        for ticket_type in ticket_types:
            data.append({
                "id": ticket_type.id,
                "nombre": ticket_type.nombre,
            })

        return Response(
            data,
            status=status.HTTP_200_OK
        )
    
class TicketTypeGiftsView(APIView):

    def get(self, request, ticket_type_id):

        service = TicketTypeService()

        ticket_type = service.get_by_id(ticket_type_id)

        if not ticket_type:
            return Response(
                {
                    "message": "Tipo de ticket no encontrado",
                    "error": "TICKET_TYPE_NOT_FOUND",
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "id": ticket_type.id,
                "nombre": ticket_type.nombre,
                "regalos": ticket_type.regalos,
            },
            status=status.HTTP_200_OK
        )