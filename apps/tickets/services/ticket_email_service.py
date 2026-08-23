import io
import qrcode

from django.core.mail import EmailMessage


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

        email = EmailMessage(
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

        email.attach(
            f"{ticket.code}.png",
            qr_buffer.getvalue(),
            "image/png"
        )

        email.send(
            fail_silently=False
        )