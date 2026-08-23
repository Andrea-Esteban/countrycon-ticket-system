from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.tickets.serializers import BuyerSerializer
from apps.tickets.services.buyer_service import BuyerService
from rest_framework.permissions import IsAuthenticated

from apps.tickets.permissions import IsAdmin


class BuyerView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin,
    ]
    def put(self, request, buyer_id):

        return self._update(
            request,
            buyer_id,
            partial=False
        )


    def patch(self, request, buyer_id):

        return self._update(
            request,
            buyer_id,
            partial=True
        )


    def _update(self, request, buyer_id, partial=False):

        service = BuyerService()

        buyer = service.get_by_id(
            buyer_id
        )

        if not buyer:
            return Response(
                {
                    "message": "Comprador no encontrado"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BuyerSerializer(
            buyer,
            data=request.data,
            partial=partial
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            buyer = service.update(
                buyer,
                serializer.validated_data,
                request.user
            )

            response_serializer = BuyerSerializer(
                buyer
            )

            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK
            )

        except ValueError as error:

            return Response(
                {
                    "message": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request, buyer_id=None):

        service = BuyerService()

        if buyer_id is not None:

            buyer = service.get_by_id(buyer_id)

            if not buyer:
                return Response(
                    {
                        "message": "Comprador no encontrado"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = BuyerSerializer(buyer)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        buyers = service.get_all()

        serializer = BuyerSerializer(
            buyers,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):

        serializer = BuyerSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            service = BuyerService()

            buyer = service.create(
                serializer.validated_data,
                request.user
            )

            response_serializer = BuyerSerializer(
                buyer
            )

            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        except ValueError as error:

            return Response(
                {
                    "message": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )