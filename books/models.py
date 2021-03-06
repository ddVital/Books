from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Books(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    cover = models.ImageField(upload_to="media/books/", default=None, null=True)
    title = models.CharField(max_length=200, blank=False)
    authors = models.CharField(max_length=200)
    pages = models.IntegerField()

    def __str__(self):
        return f"{ self.title } writen by { self.authors }"


class Wishlist(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE, related_name="user_wishlist")
    books = models.ManyToManyField(Books)

    def __str__(self) -> str:
        return f"{self.user}"


class User(AbstractUser):
    books = models.ManyToManyField(Books)
    wishlist = models.ForeignKey(Wishlist, null=True, on_delete=models.CASCADE, related_name="books_wishlist")

    def __str__(self):
        return self.username