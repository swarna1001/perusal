from django import forms
from .models import Comment, Post


class NewPostForm(forms.ModelForm):
	text_post = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Write Something...", "cols":30, "rows":8}))
	class Meta:
		model = Post
		fields = ['text_post', 'add_image']

class NewCommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['comment']


