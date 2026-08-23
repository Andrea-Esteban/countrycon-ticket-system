# apps/tickets/views/login_view.py

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if not user.is_active:
                return render(
                    request,
                    "login.html",
                    {
                        "error": "Tu usuario está desactivado."
                    }
                )

            login(request, user)

            return redirect("home")

        return render(
            request,
            "login.html",
            {
                "error": "Usuario o contraseña incorrectos."
            }
        )

    return render(
        request,
        "login.html"
    )


def logout_view(request):

    logout(request)

    return redirect("login")