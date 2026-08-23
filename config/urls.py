"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# config/urls.py

from django.contrib import admin
from django.urls import include, path

from apps.tickets.views import buyers_page
from apps.tickets.views.ticket_page_view import tickets_page
from apps.tickets.views.home_view import home_view
from apps.tickets.views.login_view import login_view, logout_view
from apps.tickets.views.scanner_view import scanner_view
from apps.tickets.views.users_page_view import users_page

urlpatterns = [

    # HTML
    path("", home_view, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("buyers/", buyers_page, name="buyers"),
    path("tickets/", tickets_page, name="tickets"),
    path("scanner/", scanner_view, name="scanner"),

    # Admin
    path("admin/", admin.site.urls),

    # API
    path("api/", include("apps.tickets.urls")),

    path(
        "users/",
        users_page,
        name="users"
    ),
]