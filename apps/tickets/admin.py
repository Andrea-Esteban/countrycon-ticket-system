from django.contrib import admin
from .forms import TicketAdminForm, BuyerAdminForm
from .models import Perfil, User, Buyer, TicketType, Ticket
from django.contrib.auth.admin import UserAdmin

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "nombre",
    )


@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
    )

    search_fields = (
        "nombre",
    )


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):

    form = TicketAdminForm

    class Media:
        js = (
            "tickets/js/ticket_admin.js",
        )

    list_display = (
        "id",
        "code",
        "buyer",
        "ticket_type",
        "is_paid",
        "is_used",
        "used_at",
        "created_at",
    )

    list_filter = (
        "ticket_type",
        "is_paid",
        "is_used",
    )
    
    search_fields = (
        "code",
        "id_qr",
        "buyer__dni",
        "buyer__nombre",
        "buyer__apellido_paterno",
    )

    readonly_fields = (
        "id_qr",
        "used_at",
        "created_at",
        "updated_at",
    )

@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "id",
        "username",
        "perfil",
        "is_active",
        "is_staff",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "perfil",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    search_fields = (
        "username",
        "email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "last_login",
    )

@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):

    form = BuyerAdminForm

    list_display = (
        "id",
        "nombre",
        "apellido_paterno",
        "apellido_materno",
        "dni",
        "email",
        "parthen",
        "partner",
        "created_at",
    )

    list_filter = (
        "parthen",
    )

    search_fields = (
        "nombre",
        "apellido_paterno",
        "apellido_materno",
        "dni",
        "email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )