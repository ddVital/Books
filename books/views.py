import os, re
from django.shortcuts import render

from django import forms
from django.contrib.auth import authenticate, update_session_auth_hash, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Books, User


# index function
def index(request):
    return render(request, 'books/index.html')


def login_view(request):
    if request.method == "POST":
        
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auth/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auth/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def password_check(password):
    """
    Verify the strength of 'password'
    """

    # calculating the length
    length_error = len(password) < 8

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(r"\W", password) is None

    # overall result
    password_ok = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error )

    return password_ok


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirm-password"]

        if password != confirmation:
            return render(request, "auth/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        if password_check(password):
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError:
                return render(request, "auth/register.html", {
                    "message": "Username already taken."
                })
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auth/register.html")