from django.urls import path

from apps.tickets.views.qr_view import QRValidationView
from apps.tickets.views.ticket_type_view import (
    TicketTypeListView,
    TicketTypeGiftsView,
)
from apps.tickets.views.buyer_view import BuyerView
from apps.tickets.views.ticket_view import TicketView
from apps.tickets.views.user_view import (
    UserView,
    UserDetailView,
)
from apps.tickets.views.perfil_view import PerfilView
urlpatterns = [
    # =========================
    # QR
    # =========================

    path(
        "qr/validate/",
        QRValidationView.as_view(),
        name="qr-validate",
    ),

    # =========================
    # TICKET TYPES
    # =========================

    path(
        "ticket-types/",
        TicketTypeListView.as_view(),
        name="ticket-types",
    ),

    path(
        "ticket-types/<int:ticket_type_id>/gifts/",
        TicketTypeGiftsView.as_view(),
        name="ticket-type-gifts",
    ),

    # =========================
    # BUYERS
    # =========================

    path(
        "buyers/",
        BuyerView.as_view(),
        name="buyer-create",
    ),

    path(
        "buyers/<int:buyer_id>/",
        BuyerView.as_view(),
        name="buyer-detail",
    ),

    # =========================
    # TICKETS
    # =========================

    path(
        "tickets/",
        TicketView.as_view(),
        name="ticket-list",
    ),

    path(
        "tickets/<int:ticket_id>/",
        TicketView.as_view(),
        name="ticket-detail",
    ),

    path(
        "users/",
        UserView.as_view(),
        name="user-list"
    ),

    path(
        "users/<int:user_id>/",
        UserDetailView.as_view(),
        name="user-detail"
    ),

    path(
        "perfiles/",
        PerfilView.as_view(),
        name="perfil-list"
    ),
]