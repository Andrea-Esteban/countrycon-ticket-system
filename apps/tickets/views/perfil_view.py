from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.tickets.serializers import PerfilSerializer
from apps.tickets.services.perfil_service import PerfilService


class PerfilView(APIView):

    def get(self, request):

        service = PerfilService()

        perfiles = service.get_all()

        serializer = PerfilSerializer(
            perfiles,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )