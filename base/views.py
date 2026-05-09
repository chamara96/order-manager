from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render

from .forms import LoginForm, RegisterForm


def handler404(request, *args, **kwargs):
    return render(request, "pages/404.html", status=404)


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("shops:index")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, "pages/auth/register.html", {"form": form})


def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(request, email=email, password=password)

            if user:
                login(request, user)
                return redirect("shops:index")

            messages.error(request, "Invalid credentials")

    return render(request, "pages/auth/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")
