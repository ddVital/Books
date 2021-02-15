from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('books/add/<str:id>', views.add_to_read_books, name="add_to_read_books"),
    path('books/remove/<str:id>', views.remove_from_read_books, name="remove_from_read_books"),
    path('wishlist/add/<str:id>', views.add_to_want_to_read, name="add_to_want_to_read"),
    path('wishlist/remove/<str:id>', views.remove_from_want_to_read, name="remove_from_want_to_read"),
    path('search', views.search, name="search"),
    path('register/', views.register, name="register"),
    path('login/', views.login_view, name="login"),
]