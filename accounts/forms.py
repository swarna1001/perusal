from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from . models import Profile, BookCategory


class RegisterForm(UserCreationForm):
	email = forms.EmailField()
	
	class Meta:
		model = User
		fields = ["username", "email", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
	username = forms.CharField(required=False)
	email = forms.EmailField(required=False)

	class Meta:
		model = User
		fields = ["username", "email"]

class ProfileImageUpdateForm(forms.ModelForm):
	image = forms.ImageField(required=False)

	class Meta:
		model = Profile
		fields = ['image']

class ProfileUpdateForm(forms.ModelForm):
	city = forms.CharField(required=False)
	state = forms.CharField(required=False)
	bio = forms.CharField(required=False)
	


	class Meta:
		model = Profile
		fields = ["city", "state", "bio"]


"""class GenresChoiceForm(forms.ModelForm):

	genre_1 = forms.ModelChoiceField(queryset=BookCategory.objects.all())
	genre_2 = forms.ModelChoiceField(queryset=BookCategory.objects.all())
	genre_3 = forms.ModelChoiceField(queryset=BookCategory.objects.all())
	genre_4 = forms.ModelChoiceField(queryset=BookCategory.objects.all())
	genre_5 = forms.ModelChoiceField(queryset=BookCategory.objects.all())

	class Meta:
		model = Profile
		fields = ['genre_1', "genre_2", "genre_3", "genre_4", 'genre_5']"""



"""class GenresChoiceForm(forms.Form):
	has_autobiography = forms.BooleanField()
	has_biography = forms.BooleanField()
	has_drama = forms.BooleanField()
	has_fairytale = forms.BooleanField()
	
	

	class Meta:
		model = Genre
		fields = ['has_autobiography', 'has_biography', 'has_drama', 'has_fairytale', 
		'has_fantasy', 'has_folktale'] """




