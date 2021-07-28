from django.contrib import admin
from .models import Profile, FriendRequest, BookCategory, Book, UserReadList, UserGenres


admin.site.register(Profile)
admin.site.register(FriendRequest)
admin.site.register(BookCategory)
admin.site.register(Book)
admin.site.register(UserReadList)
admin.site.register(UserGenres)
