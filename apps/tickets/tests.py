from django.test import TestCase
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
# Create your tests here.
