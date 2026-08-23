import json

from django import forms

from .models import Ticket, TicketType, Buyer

class BuyerAdminForm(forms.ModelForm):

    class Meta:
        model = Buyer
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # No permitir que un comprador sea su propio partner
        if self.instance and self.instance.pk:
            self.fields["partner"].queryset = Buyer.objects.exclude(
                pk=self.instance.pk
            )
        else:
            self.fields["partner"].queryset = Buyer.objects.all()

    def clean(self):
        cleaned_data = super().clean()

        parthen = cleaned_data.get("parthen")
        partner = cleaned_data.get("partner")

        # Si tiene partner, debe estar marcado como parthen
        if parthen and not partner:
            self.add_error(
                "partner",
                "Debes seleccionar un partner."
            )

        # Si no tiene partner, no debería tener partner asignado
        if not parthen and partner:
            self.add_error(
                "partner",
                "Si Parthen está desactivado, no puedes seleccionar un partner."
            )

        return cleaned_data
    
class TicketAdminForm(forms.ModelForm):

    llavero = forms.ChoiceField(
        required=False,
        choices=[],
        label="Llavero"
    )

    class Meta:
        model = Ticket
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ocultamos el JSON original
        self.fields["gift_selections"].widget = forms.HiddenInput()

        ticket_type = None

        # Si estamos enviando el formulario, usamos el
        # ticket_type que viene en el POST.
        if self.data.get("ticket_type"):
            try:
                ticket_type = TicketType.objects.get(
                    id=self.data.get("ticket_type")
                )
            except TicketType.DoesNotExist:
                ticket_type = None

        # Si no estamos enviando el formulario,
        # usamos el ticket_type actual del ticket.
        elif self.instance.pk:
            ticket_type = self.instance.ticket_type

        if ticket_type and ticket_type.regalos:

            llavero = ticket_type.regalos.get("llavero")

            if llavero:

                self.fields["llavero"].choices = [
                    ("", "---------"),
                    *[
                        (pais, pais)
                        for pais in llavero.get("list", [])
                    ]
                ]

        # Recuperar selección existente
        if self.instance.pk and self.instance.gift_selections:

            self.fields["llavero"].initial = (
                self.instance.gift_selections.get("llavero")
            )

    def save(self, commit=True):

        ticket = super().save(commit=False)

        llavero = self.cleaned_data.get("llavero")

        if llavero:
            ticket.gift_selections = {
                "llavero": llavero
            }
        else:
            ticket.gift_selections = None

        if commit:
            ticket.save()

        return ticket