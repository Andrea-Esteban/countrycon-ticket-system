# apps/tickets/serializers.py

from rest_framework import serializers
from .models import Buyer, Ticket
from .services.ticket_service import TicketService
from apps.tickets.models import Perfil, User


class QRValidationSerializer(serializers.Serializer):

    # qr = serializers.CharField(
    #     required=True,
    #     allow_blank=False,
    # )

    id_qr = serializers.UUIDField()

class BuyerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Buyer
        fields = (
            "id",
            "nombre",
            "apellido_paterno",
            "apellido_materno",
            "dni",
            "celular",
            "instagram",
            "email",
            "parthen",
            "partner",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

class TicketSerializer(serializers.ModelSerializer):

    buyer_id = serializers.IntegerField(
        write_only=True
    )

    ticket_type_id = serializers.IntegerField(
        write_only=True
    )

    class Meta:
        model = Ticket

        fields = (
            "id",
            "id_qr",
            "code",
            "buyer_id",
            "ticket_type_id",
            "gift_selections",
            "is_paid",
            "is_used",
            "used_at",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "id_qr",
            "code",
            "is_used",
            "used_at",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):

        buyer_id = validated_data.pop(
            "buyer_id"
        )

        ticket_type_id = validated_data.pop(
            "ticket_type_id"
        )

        gift_selections = validated_data.pop(
            "gift_selections",
            {}
        )

        user = self.context["request"].user

        service = TicketService()

        return service.create_ticket(
            buyer_id=buyer_id,
            ticket_type_id=ticket_type_id,
            gift_selections=gift_selections,
            user=user
        )

    def update(self, instance, validated_data):

        if "is_paid" in validated_data:

            is_paid = validated_data.pop(
                "is_paid"
            )

            if is_paid:

                service = TicketService()

                result = service.mark_as_paid(
                    ticket_id=instance.id,
                    user=self.context["request"].user
                )

                return result["ticket"]

        return super().update(
            instance,
            validated_data
        )

class UserSerializer(serializers.ModelSerializer):

    perfil = serializers.PrimaryKeyRelatedField(
        queryset=Perfil.objects.all(),
        allow_null=True,
        required=False,
    )

    perfil_nombre = serializers.CharField(
        source="perfil.nombre",
        read_only=True,
    )

    password = serializers.CharField(
        write_only=True,
        required=False,
        min_length=6,
    )

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "password",
            "perfil",
            "perfil_nombre",
            "is_active",
        ]

        read_only_fields = [
            "id",
            "perfil_nombre",
        ]

    def validate_username(self, value):

        user_id = self.instance.id if self.instance else None

        queryset = User.objects.filter(
            username=value
        )

        if user_id:
            queryset = queryset.exclude(
                id=user_id
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "El nombre de usuario ya existe."
            )

        return value

class PerfilSerializer(serializers.ModelSerializer):

    class Meta:
        model = Perfil
        fields = (
            "id",
            "nombre",
        )