import os, re, requests
from django.shortcuts import render

from django.db import IntegrityError
from django import forms
from django.contrib.auth import authenticate, update_session_auth_hash, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Books, User, Wishlist

# user = User.objects.get(username=request.user.username)

# index function
def index(request):
    user = User.objects.get(username=request.user.username)
    return render(request, 'books/index.html', {
        "books": API_request("why we sleep"),
        "read_books": read_books(user),
        "want_to_read": want_to_read_list(user),
    })


def book(request, id):
    return render(request, 'books/book-page.html', {"book": get_specific_book(id)})


def read_books(user):
    read_books = []
    for book in user.books.all():
        read_books.append(book.id)
    return read_books


def want_to_read_list(user):
    wishlist = Wishlist.objects.get(user=user)
    want_to_read = []
    for book in wishlist.books.all():
        want_to_read.append(book.id)
    return want_to_read


def API_request(search):
    r = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={search}&maxResults=40')
    data = r.json()
    return data


def get_specific_book(id):
    r = requests.get(f'https://www.googleapis.com/books/v1/volumes/{id}')
    data = r.json()
    return data


def search(request):
    search = request.GET.get('q')
    user = User.objects.get(username=request.user.username)

    return render(request, 'books/index.html', {
        "books": API_request(search),
        "read_books": read_books(user),
    })


def want_to_read(request):
    user = User.objects.get(username=request.user.username)
    books_list = Wishlist.objects.get(user=user)
    return render(request, "books/want-to-read.html", {
        "books": books_list,
    })


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

    # searching for symbolswishlist=''
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
        
        if password == '' or confirmation == '' or username == '' or email == '':
            return render(request, "auth/register.html", {
                "message": "please fill all the fields."
            })

        # Attempt to create new user
        if password_check(password):
            try:
                user = User.objects.create_user(username.lower(), email.lower(), password)
                user.save()
                create_user_wishlist(user)
            except IntegrityError:
                return render(request, "auth/register.html", {
                    "message": "Username already taken."
                })
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auth/register.html")


def profile(request):
    user = User.objects.get(username=request.user.username)
    return render(request, "books/profile.html", {
        "books": user.books.all(),
        "want_to_read": user.wishlist.books.all(),
        "total_read_pages": total_read_pages(user)
    })


def total_read_pages(user):
    total_read_pages = 0
    for book in user.books.all():
        total_read_pages += book.pages
    
    return total_read_pages


def create_book(id):
    book = get_specific_book(id)
    new_book = Books()
    
    new_book.id = book["id"]
    new_book.cover = book["volumeInfo"]["imageLinks"]["thumbnail"]
    new_book.title = book["volumeInfo"]["title"]
    new_book.authors = ', '.join(book["volumeInfo"]["authors"])
    new_book.pages = book["volumeInfo"]["pageCount"]
    new_book.save()


def create_user_wishlist(user):
    Wishlist.objects.create(user=user)
    user.wishlist = Wishlist.objects.get(user=user)
    user.save()


def add_to_read_books(request, id):
    user = User.objects.get(username=request.user.username)

    if Books.objects.filter(pk=id):
        book = Books.objects.get(pk=id)
        user.books.add(book)
    else:
        create_book(id)
        book = Books.objects.get(pk=id)
        user.books.add(book)

    return HttpResponseRedirect(reverse("index"))    


def remove_from_read_books(request, id):
    user = User.objects.get(username=request.user.username)
    book = Books.objects.get(pk=id)
    user.books.remove(book)
    return HttpResponseRedirect(reverse("index"))    


def add_to_want_to_read(request, id):
    user = User.objects.get(username=request.user.username)
    wishlist = Wishlist.objects.get(user=user)
    
    if Books.objects.filter(pk=id):
        book = Books.objects.get(pk=id)
        wishlist.books.add(book)
    else:
        create_book(id)
        book = Books.objects.get(pk=id)
        wishlist.books.add(book)

    return HttpResponseRedirect(reverse("index"))


def remove_from_want_to_read(request, id):
    wishlist = Wishlist.objects.get(user=request.user)
    book = Books.objects.get(pk=id)
    wishlist.books.remove(book)

    return HttpResponseRedirect(reverse("index"))