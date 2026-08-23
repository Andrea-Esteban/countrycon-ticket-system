from unittest.mock import patch

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from apps.tickets.models import (
    User,
    Perfil,
    Buyer,
    TicketType,
    Ticket,
)
class TicketAPITest(APITestCase):

    def setUp(self):

        self.perfil = Perfil.objects.create(
            nombre="ADMIN"
        )

        self.user = User.objects.create_user(
            username="admin",
            password="123456"
        )

        self.user.perfil = self.perfil
        self.user.is_staff = True
        self.user.save()

        self.client.force_authenticate(
            user=self.user
        )

        self.buyer = Buyer.objects.create(
            nombre="Juan",
            apellido_paterno="Perez",
            apellido_materno="Gomez",
            dni="12345678",
            celular="999999999",
            email="juan@gmail.com",
            created_by=self.user,
            updated_by=self.user,
        )

        self.ticket_type = TicketType.objects.create(
            nombre="General",
            regalos=None,
            created_by=self.user,
            updated_by=self.user,
        )

        self.vip_type = TicketType.objects.create(
            nombre="VIP",
            regalos={
                "llavero": {
                    "cant": 1,
                    "list": [
                        "Perú",
                        "Chile",
                        "USA",
                        "Rusia",
                        "USSR",
                        "Third Reich",
                    ],
                }
            },
            created_by=self.user,
            updated_by=self.user,
        )

    def test_create_ticket(self):

        data = {
            "buyer_id": self.buyer.id,
            "ticket_type_id": self.ticket_type.id,
        }

        response = self.client.post(
            "/api/tickets/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Ticket.objects.filter(
                buyer=self.buyer,
                ticket_type=self.ticket_type
            ).exists()
        )

    def test_create_vip_ticket_with_gift(self):

        data = {
            "buyer_id": self.buyer.id,
            "ticket_type_id": self.vip_type.id,
            "gift_selections": {
                "llavero": "Perú"
            },
        }

        response = self.client.post(
            "/api/tickets/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        ticket = Ticket.objects.get(
            buyer=self.buyer,
            ticket_type=self.vip_type
        )

        self.assertEqual(
            ticket.gift_selections["llavero"],
            "Perú"
        )

    def test_create_ticket_buyer_not_found(self):

        data = {
            "buyer_id": 99999,
            "ticket_type_id": self.ticket_type.id,
        }

        response = self.client.post(
            "/api/tickets/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_create_ticket_type_not_found(self):

        data = {
            "buyer_id": self.buyer.id,
            "ticket_type_id": 99999,
        }

        response = self.client.post(
            "/api/tickets/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )


    @patch(
        "apps.tickets.services.ticket_service.TicketEmailService.send_ticket_email"
    )
    def test_mark_ticket_as_paid(
        self,
        mock_send_email
    ):

        ticket = Ticket.objects.create(
            code="TEST-000001",
            buyer=self.buyer,
            ticket_type=self.ticket_type,
            is_paid=False,
            created_by=self.user,
            updated_by=self.user,
        )

        response = self.client.patch(
            f"/api/tickets/{ticket.id}/",
            {
                "is_paid": True
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        ticket.refresh_from_db()

        self.assertTrue(
            ticket.is_paid
        )

        mock_send_email.assert_called_once_with(
            ticket
        )

    @patch(
        "apps.tickets.services.ticket_service.TicketEmailService.send_ticket_email"
    )
    def test_paid_ticket_does_not_send_email_again(
        self,
        mock_send_email
    ):

        ticket = Ticket.objects.create(
            code="TEST-000002",
            buyer=self.buyer,
            ticket_type=self.ticket_type,
            is_paid=True,
            created_by=self.user,
            updated_by=self.user,
        )

        response = self.client.patch(
            f"/api/tickets/{ticket.id}/",
            {
                "is_paid": True
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        mock_send_email.assert_not_called()


    def test_update_ticket_not_found(self):

        response = self.client.patch(
            "/api/tickets/99999/",
            {
                "is_paid": True
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )