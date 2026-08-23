from apps.tickets.repositories.buyer_repository import BuyerRepository


class BuyerService:

    def __init__(self):
        self.buyer_repository = BuyerRepository()

    def get_by_id(self, buyer_id):
        return self.buyer_repository.get_by_id(buyer_id)

    def get_by_dni(self, dni):
        return self.buyer_repository.get_by_dni(dni)

    def get_all(self):
        return self.buyer_repository.get_all()

    def create(self, data, user):

        dni = data.get("dni")

        # DNI duplicado
        if self.get_by_dni(dni):
            raise ValueError(
                "Ya existe un comprador registrado con ese DNI."
            )

        parthen = data.get("parthen", False)
        partner = data.get("partner")

        # Si tiene acompañante
        if parthen:

            if not partner:
                raise ValueError(
                    "Debe seleccionar un acompañante."
                )

            # No puede ser él mismo
            if partner.id == data.get("id"):
                raise ValueError(
                    "El comprador no puede ser su propio acompañante."
                )

        # Si no tiene acompañante, limpiamos partner
        else:
            partner = None

        data["partner"] = partner
        data["created_by"] = user
        data["updated_by"] = user

        return self.buyer_repository.create(**data)


    def update(self, buyer, data, user):

        if "dni" in data:

            existing_buyer = self.get_by_dni(
                data["dni"]
            )

            if existing_buyer and existing_buyer.id != buyer.id:
                raise ValueError(
                    "Ya existe un comprador registrado con ese DNI."
                )

        parthen = data.get(
            "parthen",
            buyer.parthen
        )

        partner = data.get(
            "partner",
            buyer.partner
        )

        if parthen and not partner:
            raise ValueError(
                "Debe seleccionar un acompañante."
            )

        if not parthen:
            data["partner"] = None

        data["updated_by"] = user

        return self.buyer_repository.update(
            buyer,
            **data
        )