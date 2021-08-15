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
    path('read-list/remove-book/<int:id>/', views.remove_books, name="remove_books"),

    path('add-book/<int:id>/', views.add_book_from_homepage, name="add_book_from_homepage"), 
    path('add-book-from-genre/<int:id>/', views.add_book_based_on_genre, name="add_book_from_genre"),


    path('genre/books/<int:id>/', views.show_book_by_genres, name="books_by_genre"),

    path('search/', views.show_search_result, name="show_search_result"),

    path('genres/add-genre/<int:id>/', views.add_top_genres, name="add_top_genres"),

    #path('friends/friend-request/delete/<int:id>/', views.delete_friend_request_from_friend_list, 
        #name='delete_friend_request'),


    #path('homepage/friend-request/send/<int:id>/', views.send_friend_request_from_homepage, 
        #name='request_friend'),
    
    #url(r'^friends/delete/<int:id>/$', views.delete_friend, name='delete_friend'),

    #path('friend/delete/<int:id>/', views.delete_friend_visiting_profile, 
	#	name='remove_friend'),


]


