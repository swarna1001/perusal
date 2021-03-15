from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Profile, FriendRequest

# add Post model to the feed app

from feed.models import Post
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpResponseRedirect
import random

from django.db.models import Q

User = get_user_model()

# Generic view

def signup_view(request):
	if request.method == "POST":
		form = RegisterForm(request.POST)

		if form.is_valid():
			user = form.save()

			# log the user in
			login(request, user)
			# user is directed to his homepage, after successful login
			# return redirect('home:homepage')

			# user is directed to login page after the successful registration
			return redirect('accounts:login')


	else:
		form = RegisterForm()
	
	return render(request, 'accounts/register.html', {'form':form})


def login_view(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():

			#log in the user
			user = form.get_user()
			login(request, user)

			return redirect('accounts:homepage')
	else:
		form = AuthenticationForm()

	return render(request, 'accounts/login.html', {'form':form})


def logout_view(request):
	if request.method == 'POST':
		logout(request)

		# temporary logout direct
		# might create a different logout view

		#return redirect('basic_home/')
		return render(request, 'accounts/logout.html')



def homepage_view(request):

	# v1.0 (only 10 people in suggested window (will be scaled later))


	# REMOVE SUPERUSER----------------------->

	# location - 3 (5 for now)
	# random users (for now) - 10
	#-------------------------------------
	# genres - 3
	# friend's friend - 2
	# same read_list - 2

	# user's location
	user_loc = request.user.profile.city

	#new_list = Profile.objects.filter(city = user_loc).exclude(friends = request.user.profile)
	#print("NEW ::::", new_list)

	# WORKING QUERY - 1, queries same location users which are not friends
	new_list_2 = Profile.objects.filter(city = user_loc).exclude(friends = request.user.profile).exclude(user=request.user)
	#print("NEW AGAIN::::", new_list_2)

	# randomized and limited to 5 (sent to template)
	location_suggest = random.sample(list(new_list_2), min(len(list(new_list_2)), 5))



	not_friends = Profile.objects.exclude(friends = request.user.profile)
	not_friends_suggest_list = not_friends.exclude(user = request.user)

	# WORKING QUERY - 2, NOT friends NOT same location
	not_friend_neither_location = not_friends_suggest_list.exclude(city=user_loc)
	#print(not_friend_neither_location)

	# randomized and limited to 10 (sent to template)
	not_friend_neither_location_list = random.sample(list(not_friend_neither_location), 
		min(len(list(not_friend_neither_location)), 10))






	#----------------PERFECTLY WORKING -------------------

	posts = Post.objects.all().order_by('date_posted').exclude(user_name = request.user)




	# user genres
	current_user_genres = request.user.profile.genres

	# user genres list form
	current_user_genres_list = list(current_user_genres.split("  "))
	# sorted genres list
	sorted_genre_list = sorted(current_user_genres_list)

	"""length_sorted_genre = len(sorted_genre_list)


	if length_sorted_genre >= 2:
		gen_list = Profile.objects.filter(Q(genres = sorted_genre_list[0]) | Q(genres = sorted_genre_list[1]))

		gen_list2 = Profile.objects.filter(genres = current_user_genres)
		print(gen_list)"""







	context = {
			'location_suggest' : location_suggest,
			'not_friend_neither_location_list' : not_friend_neither_location_list,

	}

	return render(request, 'accounts/test_homepage.html', context)




	
# CHANGED ON 11/03
"""@login_required
def homepage_view(request):

	# Suggest Users is a MESS

	users = Profile.objects.exclude(user = request.user)
	sent_friend_requests = FriendRequest.objects.filter(from_user = request.user)
	print("1", users)
	print("2", sent_friend_requests)
	sent_to = []
	friends = []
	for user in users:
		friend = user.friends.all()	
		for f in friend:
			if f in friends:
				friend = friend.exclude(user = f.user)
		friends += friend
	print("3", friends)
	my_friends = request.user.profile.friends.all()
	for i in my_friends:
		if i in friends:
			friends.remove(i)
	if request.user.profile in friends:
		friends.remove(request.user.profile)
	random_list = random.sample(list(users), min(len(list(users)), 10))
	for r in random_list:
		if r in friends:
			random_list.remove(r)
	friends += random_list
	for i in my_friends:
		if i in friends:
			friends.remove(i)		
	for sent in sent_friend_requests:
		sent_to.append(sent.to_user)"""


	# USER'S POST

""" posts = Post.objects.all().order_by('date_posted')
	user_friends = request.user.profile.friends.all()
	print("FRIENDS :", user_friends)
	display_post = []
	for f in user_friends:
		temp = f.user
		for post in posts:
			temp2 = post.user_name
			if (temp == temp2):
				required_post = Post.objects.filter(user_name=temp2)

				print("POST BY USERS : ", temp2)

				display_post += [temp2]"""
	
""" display_post = []
	user_friends = request.user.profile.friends.all()
	for f in user_friends:
		temp = f.user
		posts = Post.objects.filter(user_name=f.user)

		print("POSTS BY :", posts)
		


	print("111111111111111111111", display_post)
	print("222222222222222222", friends)


	all_of = Post.objects.all()
	print("66666666666666666666", all_of)

	print(type(posts))
	print(type(display_post))
	print(type(friends))
	print(type(users))"""

"""	context = {
			'users' : friends,
			'sent' : sent_to,
			#'posts' : posts

	}
	return render(request, 'accounts/test_homepage.html', context)"""




###### BEFORE 11/03

"""@login_required
def homepage_view(request):

	# Suggest Users is a MESS

	users = Profile.objects.exclude(user = request.user)
	sent_friend_requests = FriendRequest.objects.filter(from_user = request.user)
	sent_to = []
	friends = []
	for user in users:
		friend = user.friends.all()	
		print(friend)
		for f in friend:
			if f in friends:
				friend = friend.exclude(user = f.user)

		friends += friend

	#print("USERS : ", users)
	#print("1.  ", friends)

	my_friends = request.user.profile.friends.all()
	#print("2.  ", my_friends)

	for i in my_friends:
		if i in friends:
			friends.remove(i)

	if request.user.profile in friends:
		friends.remove(request.user.profile)

	random_list = random.sample(list(users), min(len(list(users)), 10))
	#print("3.  ", random_list)

	for r in random_list:
		if r in friends:
			random_list.remove(r)

	friends += random_list

	#print("4.  ", friends)
	for i in my_friends:
		if i in friends:
			friends.remove(i)

	#print("5.  ", friends)		
	for sent in sent_friend_requests:
		sent_to.append(sent.to_user)

	context = {
			'users' : friends,
			'sent' : sent_to
	}

	#print("6.  ", friends)
	return render(request, 'accounts/test_homepage.html', context)"""




"""@login_required
def genres_view(request):
	current_user = request.user
	if request.method == "POST":
		if request.POST.get('genres'):
			savedata = current_user.profile
			savedata.genres = request.POST.get('genres')
			savedata.save()
			print("GENRES ARE:", savedata.genres)
			return redirect('accounts:homepage')
	else:
		return render(request, 'accounts/genres.html')"""


@login_required
def genres_view(request):
	current_user = request.user
	existing_genres = current_user.profile.genres
	print("EXISTING GENRES :", existing_genres)

	context = {
			'existing_genres' : existing_genres,
	}
	if request.method == "POST":
		if request.POST.get('genres'):
			savedata = current_user.profile
			savedata.genres = request.POST.get('genres')
			savedata.save()

			return redirect('accounts:homepage')
	else:
	
		return render(request, 'accounts/genres.html', context)

"""@login_required
def homepage_view(request):

	users = Profile.objects.exclude(user = request.user)
	sent_friend_requests = FriendRequest.objects.filter(from_user = request.user)
	sent_to = []
	friends = []
	for user in users:
		friend = user.friends.all()	
		for f in friend:
			if f in friends:
				friend = friend.exclude(user = f.user)

		friends += friend

	my_friends = request.user.profile.friends.all()
	print(my_friends)


	for i in my_friends:
		if i in friends:
			print(i)
			friends.remove(i)
	print("FRIENDS :::::::::::", friends)

	if request.user.profile in friends:
		friends.remove(request.user.profile)

	print("FRIENDS NEW LIST :::::::::::", friends)"""




	# ON USING THESE CODES, SUPERUSER PROFILE IS NOT SHOWN

""" random_list = random.sample(list(users), min(len(list(users)), 10))

	for r in random_list:
		if r in friends:
			random_list.remove(r)

	print("RANDOM :", random_list)

	friends += random_list

	for i in my_friends:
		if i in friends:
			friends.remove(i)

	for sent in sent_friend_requests:
		sent_to.append(sent.to_user)"""

""" context = {
			'users' : friends,
			'sent' : sent_to
	}

	print("USERS are", friends)
	
	return render(request, 'accounts/homepage.html', context)""" 


# recent changes
"""
@login_required
def homepage_view(request):

	users = Profile.objects.exclude(user = request.user)
	print("1")
	print(users)

	friend_count = 0
	logged_in_user_friends = []
	suggested_user_list = []

	sent_friend_requests = FriendRequest.objects.filter(from_user = request.user)
	sent_to = []
	friends = []
	for user in users:
		friend = user.friends.all()	
		print("2")
		print(friend)
		for f in friend:
			if f.user == request.user:
				friend_count = friend_count + 1
				print("3")

				print(user)
				logged_in_user_friends.append(user)

				print("FRIENDS 4444  :::::")
				print(logged_in_user_friends)
	print("5")
	print(friend_count)
	
	for frnd in users:
		for frnds in logged_in_user_friends:
			if frnd != frnds:
				suggested_user_list.append(frnd)

	print("6")
	print(suggested_user_list)


	

	# till here TESTED -------------------

	my_friends = request.user.profile.friends.all()
	print(my_friends)

	for i in my_friends:
		if i in friends:
			friends.remove(i)

	if request.user.profile in friends:
		friends.remove(request.user.profile)

	random_list = random.sample(list(users), min(len(list(users)), 10))

	for r in random_list:
		if r in friends:
			random_list.remove(r)

	friends += random_list

	for i in my_friends:
		if i in friends:
			friends.remove(i)

	for sent in sent_friend_requests:
		sent_to.append(sent.to_user)

	context = {
			'users' : suggested_user_list,
			'friend_count' : friend_count
	}

	
	return render(request, 'accounts/homepage.html', context)"""





 


@login_required
def edit_profile_view(request):
    # return HttpResponse(slug)
    if request.method == "POST":

    	u_form = UserUpdateForm(request.POST, instance=request.user)
    	p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)


    	if u_form.is_valid() and p_form.is_valid():
    		u_form.save()
    		p_form.save()

    		messages.success(request, f'your profile has been updated!')
    		return redirect('accounts:homepage')

    	else:
    		messages.success(request, f'Fill all the fields!')

    else:

	    u_form = UserUpdateForm(instance=request.user)
	    p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
    	'u_form' : u_form,
    	'p_form' : p_form,
    }

    return render(request, 'accounts/edit_profile.html', context)



#------------------------------- currently working on ----------

# users_list view used in the my_profile view

@login_required
def users_list(request):
	
	users = Profile.objects.exclude(user = request.user)
	sent_friend_requests = FriendRequest.objects.filter(from_user = request.user)
	sent_to = []
	friends = []
	for user in users:
		friend = user.friends.all()	
		for f in friend:
			if f in friends:
				friend = friend.exclude(user = f.user)

		friends += friend

	my_friends = request.user.profile.friends.all()
	for i in my_friends:
		if i in friends:
			friends.remove(i)

	if request.user.profile in friends:
		friends.remove(request.user.profile)

	random_list = random.sample(list(users), min(len(list(users)), 10))

	for r in random_list:
		if r in friends:
			random_list.remove(r)

	friends += random_list

	for i in my_friends:
		if i in friends:
			friends.remove(i)

	for sent in sent_friend_requests:
		sent_to.append(sent.to_user)

	context = {
			'users' : friends,
			'sent' : sent_to
	}

	return render(request, "accounts/users_list.html", context)


# any user's profile view
@login_required
def profile_view(request, slug):

	p = Profile.objects.filter(slug=slug).first()
	u = p.user
	sent_friend_requests = FriendRequest.objects.filter(from_user=p.user)
	rec_friend_requests = FriendRequest.objects.filter(to_user=p.user)
	#user_posts = Post.objects.filter(user_name=u)

	friends = p.friends.all()

	# is this user our friend
	button_status = 'none'
	if p not in request.user.profile.friends.all():
		button_status = 'not_friend'

		# if we have sent him a friend request
		if len(FriendRequest.objects.filter(
			from_user=request.user).filter(to_user=p.user)) == 1:
				button_status = 'friend_request_sent'

		# if we have recieved a friend request
		if len(FriendRequest.objects.filter(
			from_user=p.user).filter(to_user=request.user)) == 1:
				button_status = 'friend_request_received'

	# get genres to be displayed in the view
	current_user = p.user
	existing_genres = current_user.profile.genres
	
	context = {
		'u': u,
		'button_status': button_status,
		'friends_list': friends,
		'sent_friend_requests': sent_friend_requests,
		'rec_friend_requests': rec_friend_requests,
		'existing_genres' : existing_genres,
		#'post_count': user_posts.count
	}

	return render(request, "accounts/profile.html", context)



### need to work on ---------------------------

"""
def friend_list(request):
	p = request.user.profile

	users = Profile.objects.exclude(user = request.user)

	friend_count = 0
	logged_in_user_friends = []
	suggested_user_list = []

	for user in users:
		friend = user.friends.all()	
		print(friend)
		for f in friend:
			if f.user == request.user:
				friend_count = friend_count + 1

				print(user)
				logged_in_user_friends.append(user)

				print("FRIENDS :::::")
				print(logged_in_user_friends)

	print(friend_count)


	context = { 
		'friends' : logged_in_user_friends,
		'friend_count' : friend_count
	}
	return render (request, "accounts/friends_list.html", context) """


	


# EARLIER VERSION

def friend_list(request):
	p = request.user.profile
	friends = p.friends.all()
	context = { 
		'friends' : friends
	}
	return render (request, "accounts/friends_list.html", context)






@login_required
def send_friend_request(request, id):
	user = get_object_or_404 (User, id = id)
	frequest , created = FriendRequest.objects.get_or_create(
						from_user = request.user,
						to_user = user )

	return HttpResponseRedirect('/accounts/homepage/')


@login_required
def cancel_friend_request(request, id):
	user = get_object_or_404(User, id = id)
	frequest = FriendRequest.objects.filter(
				from_user = request.user,
				to_user = user).first()

	frequest.delete()
	return HttpResponseRedirect('/accounts/homepage/')


@login_required
def accept_friend_request(request, id):
	from_user = get_object_or_404(User, id = id)
	frequest = FriendRequest.objects.filter(from_user = from_user, to_user = request.user).first()
	user_1 = frequest.to_user
	user_2 = from_user

	user_1.profile.friends.add(user_2.profile)
	user_2.profile.friends.add(user_1.profile)

	if(FriendRequest.objects.filter(from_user = request.user, to_user = from_user).first()):
		request_received = FriendRequest.objects.filter(from_user = request.user, 
			to_user = from_user).first()

		request_received.delete()

	frequest.delete()
	return HttpResponseRedirect('/accounts/homepage/')


@login_required
def delete_friend_request(request, id):
	from_user = get_object_or_404(User, id)
	frequest = FriendRequest.objects.filter(from_user = from_user, to_user = request.user).first()
	frequest.delete()
	return HttpResponseRedirect('/accounts/homepage/')


def delete_friend_using_friends_list(request, id):
	user_profile = request.user.profile
	friend_profile = get_object_or_404(Profile, id = id)
	user_profile.friends.remove(friend_profile)
	friend_profile.friends.remove(user_profile)

	#return HttpResponseRedirect('/accounts/friend_list')
	return redirect('accounts:friend_list')


def delete_friend_visiting_profile(request, id):
	user_profile = request.user.profile
	friend_profile = get_object_or_404(Profile, id = id)
	user_profile.friends.remove(friend_profile)
	friend_profile.friends.remove(user_profile)

	return HttpResponseRedirect('/accounts/homepage/')



# renders the logged in user's profile

@login_required
def my_profile(request):
	p = request.user.profile
	you = p.user
	sent_friend_requests = FriendRequest.objects.filter(from_user = you)
	rec_friend_requests = FriendRequest.objects.filter(to_user = you)

	user_posts = Post.objects.filter(user_name = you)
	friends = p.friends.all()

