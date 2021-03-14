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

	genres = models.CharField(max_length=1000, blank=True)

	

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


