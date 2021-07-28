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

    url(r'^genres/$', views.show_genres, name="genres"),

    url(r'^read-list/$', views.show_read_list, name="read_list"),
    url(r'^read-list/update/$', views.update_read_list, name="update_read_list"),

    url(r'^edit-genres/$', views.edit_genre, name="edit_genres"),
    url(r'^friends/$', views.friend_list, name="friend_list"),


    url(r'^my_profile/$', views.my_profile, name="my_profile"),

    url(r'^my_notifications/$', views.notification_view, name="notification"),

    path('friends/friend/delete/<int:id>/', views.delete_friend_using_friends_list, 
    	name='delete_friend'),

    path('edit-genres/add-genre/<int:id>/', views.add_genres, name="add_genre"),
    path('genres/remove-genre/<int:id>/', views.remove_genres, name="remove_genre"),

    path('add-book/<int:id>/', views.add_book_from_homepage, name="add_book_from_homepage"),





    #path('friends/friend-request/delete/<int:id>/', views.delete_friend_request_from_friend_list, 
        #name='delete_friend_request'),


    #path('homepage/friend-request/send/<int:id>/', views.send_friend_request_from_homepage, 
        #name='request_friend'),
    
    #url(r'^friends/delete/<int:id>/$', views.delete_friend, name='delete_friend'),

    #path('friend/delete/<int:id>/', views.delete_friend_visiting_profile, 
	#	name='remove_friend'),


]


