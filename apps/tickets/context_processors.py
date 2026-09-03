from django.conf import settings


def global_settings(request):
    return {
        "DJANGO_BASE_URL": settings.DJANGO_BASE_URL,
    }
