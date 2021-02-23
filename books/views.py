import requests
from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Books, User, Wishlist


# index function
@login_required(login_url='/login')
def index(request):
    user = User.objects.get(username=request.user.username)
    return render(request, 'books/index.html', {
        "books": Books.objects.all(),
        "read_books": read_books(user),
        "want_to_read": want_to_read_list(user),
        "total_read_pages": total_read_pages(user)
    })


@login_required(login_url='/login')
def book(request, id):
    user = User.objects.get(username=request.user.username)
    
    try:
        return render(request, 'books/book-page.html', {
            "book": get_specific_book(id),
            "read_books": read_books(user),
            "want_to_read": want_to_read_list(user),
        })
    except Exception as e:
        return render(request, 'books/error.html', {
            "error": e.__str__()
        })


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


@login_required(login_url='/login')
def search(request):
    search = request.GET.get('q')
    user = User.objects.get(username=request.user.username)

    return render(request, 'books/search.html', {
        "results": API_request(search),
        "read_books": read_books(user),
        "total_read_pages": total_read_pages(user),
        "search": search
    })


@login_required(login_url='/login')
def want_to_read(request):
    user = User.objects.get(username=request.user.username)
    books_list = Wishlist.objects.get(user=user)
    return render(request, "books/want-to-read.html", {
        "books": books_list,
        "read_books": read_books(user),
        "want_to_read": want_to_read_list(user),
    })


@login_required(login_url='/login')
def books(request):
    user = User.objects.get(username=request.user.username)
    return render(request, "books/books.html", {
        "books": user.books.all(),
        "read_books": read_books(user),
        "want_to_read": want_to_read_list(user),
    })


def edit_profile(request):
    user = User.objects.get(username=request.user.username)

    if request.method == "POST":
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.username = request.POST["username"]
        user.email = request.POST["email"]
        user.save()

        return HttpResponseRedirect(reverse("profile"))

    return render(request, "books/edit-profile.html")


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

def delete_account(request):
    user = User.objects.get(username=request.user.username)
    user.delete()
    return HttpResponseRedirect(reverse("login_view"))


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
        if len(username) >= 4 and len(username) <= 16:
            if len(password) >= 8:
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
                return render(request, "auth/register.html", {
                    "message": "Password must be at least 8 characters"
                })
        else:
            return render(request, "auth/register.html", {
                "message": "Username must contain between 4 and 16 characters"
            })
    else:
        return render(request, "auth/register.html")


def total_read_pages(user):
    total_read_pages = 0
    for book in user.books.all():
        total_read_pages += book.pages
    
    return total_read_pages


def create_book(id):
    book = get_specific_book(id)
    new_book = Books()
    
    new_book.id = book["id"]
    try:
        new_book.cover = book["volumeInfo"]["imageLinks"]["thumbnail"]
    except:
        print('Book has no cover')
    new_book.title = book["volumeInfo"]["title"]
    try:
        new_book.authors = ', '.join(book["volumeInfo"]["authors"])
    except:
        print('authors not available')
    try:
        new_book.pages = book["volumeInfo"]["pageCount"]
    except:
        print('page count not available')

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