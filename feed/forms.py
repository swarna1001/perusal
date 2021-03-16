from django import forms
from .models import Comment, Post


class NewPostForm(forms.ModelForm):
	text_post = forms.CharField(widget=forms.Textarea)
	
	class Meta:
		model = Post
		fields = ['text_post', 'post_image', 'tags']

class NewCommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['comment']


