import io
from email.message import MIMEPart
from email.utils import make_msgid

import qrcode

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class TicketEmailService:

    def send_ticket_email(self, ticket):

        # =========================================================
        # QR
        # =========================================================

        qr = qrcode.make(
            str(ticket.id_qr)
        )

        qr_buffer = io.BytesIO()

        qr.save(
            qr_buffer,
            format="PNG"
        )

        qr_buffer.seek(0)

        qr_cid = make_msgid()

        qr_image = MIMEPart()

        qr_image.set_content(
            qr_buffer.getvalue(),
            maintype="image",
            subtype="png",
            disposition="inline",
            cid=qr_cid,
        )

        # =========================================================
        # BANNER
        # =========================================================

        banner_path = (
            settings.BASE_DIR
            / "apps"
            / "tickets"
            / "templates"
            / "email_assets"
            / "BANNER_EMAIL2.png"
        )

        banner_cid = make_msgid()

        banner_image = MIMEPart()

        with open(banner_path, "rb") as banner_file:

            banner_image.set_content(
                banner_file.read(),
                maintype="image",
                subtype="png",
                disposition="inline",
                cid=banner_cid,
            )

        # =========================================================
        # REGALO
        # =========================================================

        gift = None

        if ticket.ticket_type.nombre == "VIP":

            regalos = ticket.ticket_type.regalos or {}
            gift_selections = ticket.gift_selections or {}

            llavero = regalos.get("llavero")

            if llavero:

                gift = {
                    "type": "llavero",
                    "quantity": llavero.get("cant", 0),
                    "selection": gift_selections.get("llavero"),
                }

        # =========================================================
        # HTML
        # =========================================================

        html_content = render_to_string(
            "emails/ticket_confirmation.html",
            {
                "ticket": ticket,
                "gift": gift,

                # make_msgid() devuelve algo como:
                # <abc123@servidor>
                #
                # En HTML necesitamos:
                # abc123@servidor

                "qr_cid": qr_cid[1:-1],
                "banner_cid": banner_cid[1:-1],
            }
        )

        # =========================================================
        # EMAIL
        # =========================================================

        email = EmailMultiAlternatives(
            subject="Tu entrada para COUNTRYCON",
            body=(
                f"Hola {ticket.buyer.nombre},\n\n"
                "Tu entrada para COUNTRYCON ha sido confirmada.\n\n"
                f"Código de ticket: {ticket.code}\n"
                f"Tipo de ticket: {ticket.ticket_type.nombre}\n\n"
                "Presenta tu código QR para ingresar al evento.\n\n"
                "¡Nos vemos en COUNTRYCON!"
            ),
            to=[
                ticket.buyer.email
            ],
        )

        email.attach_alternative(
            html_content,
            "text/html"
        )

        # Imágenes INLINE
        email.attach(
            banner_image
        )

        email.attach(
            qr_image
        )

        email.send(
            fail_silently=False
        )
