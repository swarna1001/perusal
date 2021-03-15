from django.conf.urls import url, include
from .import views
from django.urls import path
from .views import PostUpdateView, PostListView, UserPostListView

app_name = 'feed'

urlpatterns = [

			url(r'^post/new/$', views.create_post, name='post-create'),
			#url(r'^post/<int:pk>/$', views.post_detail, name='post-detail'),
			path('post/detail', views.post_detail, name='post-detail'),

			#url(r'^user_posts/<str:username>/$', UserPostListView.as_view(), name='user-posts'),
			url(r'^postlist/$', PostListView.as_view(), name='post-home'),
			#path('posts/<slug>/', UserPostListView.as_view(), name='user-posts'),
			path('user_posts/<str:username>', UserPostListView.as_view(), name='user-posts'),


			




]