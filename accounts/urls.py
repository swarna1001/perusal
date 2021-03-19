from django.conf.urls import url, include
from .import views
from django.urls import path



app_name = 'accounts'

urlpatterns = [
    url(r'^signup/$', views.signup_view, name="signup"),
    url(r'^login/$', views.login_view, name="login"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^edit_profile/$', views.edit_profile_view, name="edit_profile"),
    #url(r'^my_profile/$', views.my_profile_view, name="my_profile"),

    url(r'^homepage/$', views.homepage_view, name="homepage"),

    url(r'^genres/$', views.genres_view, name="genres"),
    url(r'^friends/$', views.friend_list, name="friend_list"),


    url(r'^my_profile/$', views.my_profile, name="my_profile"),




    path('friends/friend/delete/<int:id>/', views.delete_friend_using_friends_list, 
    	name='delete_friend'),
    
    #url(r'^friends/delete/<int:id>/$', views.delete_friend, name='delete_friend'),

    #path('friend/delete/<int:id>/', views.delete_friend_visiting_profile, 
	#	name='remove_friend'),


]


