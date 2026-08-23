from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.tickets.models import Buyer, Ticket, TicketType


class QRValidationTest(APITestCase):

    def setUp(self):
        self.buyer = Buyer.objects.create(
            nombre="Andrea",
            apellido_paterno="Cordova",
            apellido_materno="Test",
            dni="12345678",
            email="andrea@test.com",
        )

        self.ticket_type = TicketType.objects.create(
            nombre="NORMAL",
            regalos=None,
        )

        self.ticket = Ticket.objects.create(
            code="CT-TEST-000001",
            buyer=self.buyer,
            ticket_type=self.ticket_type,
            is_used=False,
        )

        self.url = reverse("qr-validate")

    def test_uuid_invalido(self):
        response = self.client.post(
            self.url,
            {
                "id_qr": "123456",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_qr_inexistente(self):
        response = self.client.post(
            self.url,
            {
                "id_qr": "95fbbbd7-bf4a-4e13-938e-efdf8943b0b2",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_qr_valido_marca_ticket_como_usado(self):
        response = self.client.post(
            self.url,
            {
                "id_qr": str(self.ticket.id_qr),
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.ticket.refresh_from_db()

        self.assertTrue(self.ticket.is_used)
        self.assertIsNotNone(self.ticket.used_at)

    def test_qr_ya_utilizado(self):
        self.ticket.is_used = True
        self.ticket.save()

        response = self.client.post(
            self.url,
            {
                "id_qr": str(self.ticket.id_qr),
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_409_CONFLICT,
        )


    def test_qr_ya_utilizado_devuelve_used_at(self):
        from django.utils import timezone

        self.ticket.is_used = True
        self.ticket.used_at = timezone.now()
        self.ticket.save()

        response = self.client.post(
            self.url,
            {
                "id_qr": str(self.ticket.id_qr),
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_409_CONFLICT,
        )

        self.assertIn(
            "used_at",
            response.data,
        )

        self.assertIsNotNone(
            response.data["used_at"],
        )

        self.assertTrue(
            response.data["used_at"].endswith("-05:00"),
        )