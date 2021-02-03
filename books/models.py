from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Books(models.Model):
    cover = models.ImageField(upload_to="media/books/", default=None, null=True)
    title = models.CharField(max_length=200, blank=False)
    sub_title = models.CharField(max_length=200, blank=False)
    isbn = models.CharField(max_length=13)
    description = models.CharField(max_length=1000, null=True)
    categories = models.CharField(max_length=200)
    authors = models.CharField(max_length=200)
    publish_date = models.CharField(max_length=64)
    publisher = models.CharField(max_length=100)
    pages = models.IntegerField()

    def __str__(self):
        return f"{ self.title } writen by { self.authors }"


class Wishlist(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE, related_name="user_wishlist")
    books = models.ManyToManyField(Books)

    def __str__(self) -> str:
        return f"{self.user}: {self.books}"


class User(AbstractUser):
    avatar = models.ImageField(upload_to="media/", default=None, null=True, blank=True)
    books = models.ManyToManyField(Books, null=True)
    wishlist = models.ForeignKey(Wishlist, null=True, on_delete=models.CASCADE, related_name="books_wishlist")

    def __str__(self):
        return self.username