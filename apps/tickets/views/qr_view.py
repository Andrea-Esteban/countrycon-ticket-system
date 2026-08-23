# apps/tickets/views/qr_view.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.tickets.serializers import QRValidationSerializer
from apps.tickets.services.qr_service import QRService
# from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

from apps.tickets.permissions import IsAdminOrValidador


class QRValidationView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrValidador,
    ]
    def post(self, request):

        serializer = QRValidationSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                {
                    "valid": False,
                    "message": "UUID inválido",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        id_qr = serializer.validated_data["id_qr"]

        service = QRService()

        result = service.validate_qr(id_qr)

        if result["status"] == "not_found":
            return Response(
                result,
                status=status.HTTP_404_NOT_FOUND
            )

        if result["status"] == "already_used":
            return Response(
                result,
                status=status.HTTP_409_CONFLICT
            )

        return Response(
            result,
            status=status.HTTP_200_OK
        )