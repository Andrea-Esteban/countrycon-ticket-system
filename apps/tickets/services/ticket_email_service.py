import io
import qrcode

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from email.mime.image import MIMEImage


class TicketEmailService:

    def send_ticket_email(self, ticket):

        qr = qrcode.make(
            str(ticket.id_qr)
        )

        qr_buffer = io.BytesIO()

        qr.save(
            qr_buffer,
            format="PNG"
        )

        qr_buffer.seek(0)
        qr_image = MIMEImage(
            qr_buffer.getvalue(),
            _subtype="png"
        )

        qr_image.add_header(
            "Content-ID",
            "<ticket_qr>"
        )

        qr_image.add_header(
            "Content-Disposition",
            "inline",
            filename=f"{ticket.code}.png"
        )

        banner_path = (
            settings.BASE_DIR
            / "apps"
            / "tickets"
            / "templates"
            / "email_assets"
            / "BANNER_EMAIL.PNG"
        )

        with open(banner_path, "rb") as banner_file:
            banner = MIMEImage(
                banner_file.read(),
                _subtype="png"
            )

        banner.add_header(
            "Content-ID",
            "<BANNER_EMAIL>"
        )

        banner.add_header(
            "Content-Disposition",
            "inline",
            filename="BANNER_EMAIL.PNG"
        )

        html_content = render_to_string(
            "emails/ticket_confirmation.html",
            {
                "ticket": ticket,
            }
        )

        email = EmailMultiAlternatives(
            subject="Tu entrada para COUNTRYCON",
            body=(
                f"Hola {ticket.buyer.nombre},\n\n"
                "Tu entrada para COUNTRYCON ha sido confirmada.\n\n"
                f"Código de ticket: {ticket.code}\n"
                f"Tipo de ticket: {ticket.ticket_type.nombre}\n\n"
                "Adjuntamos tu código QR para ingresar al evento.\n\n"
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

        email.attach(banner)
        email.attach(qr_image)

        email.send(
            fail_silently=False
        )
