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
	email = forms.EmailField()
	class Meta:
		model = User
		fields = ["username", "email"]

class ProfileUpdateForm(forms.ModelForm):
	city = forms.CharField()
	state = forms.CharField()
	bio = forms.CharField()

	class Meta:
		model = Profile
		fields = ['image', "city", "state", "bio"]


class GenresChoiceForm(forms.ModelForm):

	genre_1 = forms.ModelChoiceField(queryset=BookCategory.objects.all())
	genre_2 = forms.ModelChoiceField(queryset=BookCategory.objects.all())
	genre_3 = forms.ModelChoiceField(queryset=BookCategory.objects.all())
	genre_4 = forms.ModelChoiceField(queryset=BookCategory.objects.all())
	genre_5 = forms.ModelChoiceField(queryset=BookCategory.objects.all())



"""class GenresChoiceForm(forms.Form):
	has_autobiography = forms.BooleanField()
	has_biography = forms.BooleanField()
	has_drama = forms.BooleanField()
	has_fairytale = forms.BooleanField()
	
	

	class Meta:
		model = Genre
		fields = ['has_autobiography', 'has_biography', 'has_drama', 'has_fairytale', 
		'has_fantasy', 'has_folktale'] """




