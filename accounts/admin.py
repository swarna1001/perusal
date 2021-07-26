from django.contrib import admin
from .models import Profile, FriendRequest, BookCategory, Book


admin.site.register(Profile)
admin.site.register(FriendRequest)
admin.site.register(BookCategory)
admin.site.register(Book)

