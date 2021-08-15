from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from autoslug import AutoSlugField
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
from django.conf import settings


class Profile(models.Model):

	user = models.OneToOneField(User, on_delete = models.CASCADE)
	image = models.ImageField(default = 'default.jpg', upload_to = 'profile_pics')
	city = models.CharField(max_length=30, blank=True)
	state = models.CharField(max_length=30, blank=True)
	slug = AutoSlugField(populate_from='user')
	bio = models.CharField(max_length=255, blank=True)
	friends = models.ManyToManyField("Profile", blank=True)	


	def __str__(self):
		return f'{self.user.username}'

	def get_absolute_url(self):
		return "/accounts/{}".format(self.slug)


	# for image resize and save the updated profile in the database

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		
		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)


class FriendRequest(models.Model):
	to_user = models.ForeignKey(settings.AUTH_USER_MODEL, 
		related_name='to_user', on_delete=models.CASCADE)
	
	from_user = models.ForeignKey(settings.AUTH_USER_MODEL, 
		related_name='from_user', on_delete=models.CASCADE)

	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "From {}, to {}".format(self.from_user.username, self.to_user.username)


class BookCategory(models.Model):

	category_name = models.CharField(max_length=250)
	category_rank = models.IntegerField(unique=True)
	score = models.IntegerField(default=0)

	def __str__(self):
		return self.category_name

	def get_score(self):
		return self.score


class Book(models.Model):
	name = models.CharField(max_length=500, null=False, blank=False)
	cover_img = models.ImageField(upload_to = 'book_covers')
	ISBN = models.CharField(max_length=15, null=True, blank=True)
	category = models.ForeignKey(BookCategory, related_name='get_books', on_delete=models.CASCADE)
	author = models.CharField(max_length=500,null=True, blank=True)
	score = models.IntegerField(default=0)

	def __str__(self):
		return self.name

	def get_score(self):
		return self.score

	def get_book_category(self):
		return self.category
	

class UserReadList(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='get_all_user_books')
	book = models.ForeignKey(Book, on_delete=models.CASCADE)

	def __str__(self):
		return "{}".format(self.book)


class UserGenres(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='get_all_user_genres')
	genre = models.ForeignKey(BookCategory, on_delete=models.CASCADE)

	def __str__(self):
		return "{}".format(self.genre)

		