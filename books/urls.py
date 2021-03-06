from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('search', views.search, name="search"),
    path('book/<str:id>', views.book, name="book"),
    path('books/add/<str:id>', views.add_to_read_books, name="add_to_read_books"),
    path('books/remove/<str:id>', views.remove_from_read_books, name="remove_from_read_books"),
    path('want-to-read/', views.want_to_read, name="want_to_read"),
    path('books/', views.books, name="books"),
    path('wishlist/add/<str:id>', views.add_to_want_to_read, name="add_to_want_to_read"),
    path('wishlist/remove/<str:id>', views.remove_from_want_to_read, name="remove_from_want_to_read"),
    path('user/edit', views.edit_profile, name="edit_profile"),
    path('register/', views.register, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('delete/account', views.delete_account, name="delete_account"),
]