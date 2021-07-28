from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as account_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'accounts/', include('accounts.urls')),   
    path(r'', views.basic_home_view, name="basic_home"), 
    path('accounts/<slug>/', account_views.profile_view, name='profile_view'),

    path('accounts/friend-request/send/<int:id>/', account_views.send_friend_request, 
    	name='send_friend_request'),

	path('accounts/friend-request/cancel/<int:id>/', account_views.cancel_friend_request, 
		name='cancel_friend_request'),

	path('accounts/friend-request/accept/<int:id>/', account_views.accept_friend_request, 
		name='accept_friend_request'),

	path('accounts/friend-request/delete/<int:id>/', account_views.delete_friend_request, 
		name='delete_friend_request'),

	#path('accounts/friend/delete/<int:id>/', account_views.delete_friend_visiting_profile, 
		#name='remove_friend'),

	path('accounts/friend/delete/<int:id>/', account_views.delete_friend_visiting_profile, 
		name='remove_friend'),

	path(r'feed/', include('feed.urls')),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

