from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.tickets.serializers import UserSerializer
from apps.tickets.services.user_service import UserService
from rest_framework.permissions import IsAuthenticated

from apps.tickets.permissions import IsAdmin


# class UserView(APIView):

#     def get(self, request):

#         service = UserService()

#         users = service.get_all()

#         serializer = UserSerializer(
#             users,
#             many=True
#         )

#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK
#         )

#     def post(self, request):

#         serializer = UserSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         service = UserService()

#         try:

#             user = service.create(
#                 username=serializer.validated_data["username"],
#                 password=serializer.validated_data["password"],
#                 perfil=serializer.validated_data.get("perfil"),
#                 is_active=serializer.validated_data.get(
#                     "is_active",
#                     True
#                 ),
#             )

#         except ValueError as e:

#             return Response(
#                 {
#                     "message": str(e),
#                     "error": "USER_ALREADY_EXISTS",
#                 },
#                 status=status.HTTP_409_CONFLICT
#             )

#         response_serializer = UserSerializer(user)

#         return Response(
#             response_serializer.data,
#             status=status.HTTP_201_CREATED
#         )

class UserView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):

        service = UserService()

        users = service.get_all()

        serializer = UserSerializer(
            users,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):

        serializer = UserSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        service = UserService()

        try:

            user = service.create(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
                perfil=serializer.validated_data.get("perfil"),
                is_active=serializer.validated_data.get(
                    "is_active",
                    True
                ),
            )

        except ValueError as e:

            return Response(
                {
                    "message": str(e),
                    "error": "USER_ALREADY_EXISTS",
                },
                status=status.HTTP_409_CONFLICT
            )

        response_serializer = UserSerializer(user)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )


class UserDetailView(APIView):
    permission_classes = [IsAdmin]

    def patch(self, request, user_id):

        service = UserService()

        user = service.get_by_id(user_id)

        if not user:

            return Response(
                {
                    "message": "Usuario no encontrado.",
                    "error": "USER_NOT_FOUND",
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserSerializer(
            user,
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            user = service.update(
                user=user,
                username=serializer.validated_data.get(
                    "username"
                ),
                password=serializer.validated_data.get(
                    "password"
                ),
                perfil=serializer.validated_data.get(
                    "perfil"
                ),
                is_active=serializer.validated_data.get(
                    "is_active"
                ),
            )

        except ValueError as e:

            return Response(
                {
                    "message": str(e),
                    "error": "USER_ALREADY_EXISTS",
                },
                status=status.HTTP_409_CONFLICT
            )

        response_serializer = UserSerializer(user)

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK
        )