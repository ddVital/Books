from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('search', views.search, name="search"),
    path('register/', views.register, name="register"),
    path('login/', views.login_view, name="login"),
]