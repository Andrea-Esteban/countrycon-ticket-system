import uuid

from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.db import models


class Perfil(models.Model):

    id = models.AutoField(
        primary_key=True
    )

    nombre = models.CharField(
        max_length=100
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "perfil"

    def __str__(self):
        return self.nombre


class User(AbstractUser):

    perfil = models.ForeignKey(
        Perfil,
        on_delete=models.PROTECT,
        db_column="perfil_id",
        related_name="users",
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username

class Buyer(models.Model):

    id = models.AutoField(
        primary_key=True
    )

    nombre = models.CharField(
        max_length=100
    )

    apellido_paterno = models.CharField(
        max_length=100
    )

    apellido_materno = models.CharField(
        max_length=100
    )

    dni = models.CharField(
        max_length=8,
        unique=True
    )

    celular = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    instagram = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    email = models.EmailField()

    parthen = models.BooleanField(
        default=False
    )

    partner = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        db_column="partner_id",
        related_name="partner_of",
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        db_column="created_by",
        related_name="buyers_created",
        null=True,
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        db_column="updated_by",
        related_name="buyers_updated",
        null=True,
        blank=True
    )

    class Meta:
        db_table = "buyers"

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno}"

class TicketType(models.Model):

    id = models.AutoField(
        primary_key=True
    )

    nombre = models.CharField(
        max_length=100
    )

    regalos = models.JSONField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        db_column="created_by",
        related_name="ticket_types_created",
        null=True,
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        db_column="updated_by",
        related_name="ticket_types_updated",
        null=True,
        blank=True
    )

    class Meta:
        db_table = "ticket_types"

    def __str__(self):
        return self.nombre
    
class Ticket(models.Model):

    id = models.AutoField(
        primary_key=True
    )

    id_qr = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    code = models.CharField(
        max_length=100,
        unique=True
    )

    buyer = models.ForeignKey(
        Buyer,
        on_delete=models.PROTECT,
        db_column="id_buyer",
        related_name="tickets"
    )

    ticket_type = models.ForeignKey(
        TicketType,
        on_delete=models.PROTECT,
        db_column="id_ticket_type",
        related_name="tickets"
    )
    
    gift_selections = models.JSONField(
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        default=True
    )
    is_used = models.BooleanField(
        default=False
    )

    is_paid = models.BooleanField(
        default=False
    )

    used_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        db_column="created_by",
        related_name="tickets_created",
        null=True,
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        db_column="updated_by",
        related_name="tickets_updated",
        null=True,
        blank=True
    )

    class Meta:
        db_table = "tickets"

    def __str__(self):
        return self.code