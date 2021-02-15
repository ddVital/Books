from django.contrib import admin

from .models import Books, User, Wishlist

# Register your models here.
admin.site.register(Books)
admin.site.register(User)
admin.site.register(Wishlist)