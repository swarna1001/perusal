from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm, ProfileImageUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile, FriendRequest, BookCategory, Book, UserGenres, UserReadList
from feed.models import Post
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpResponseRedirect
import random
from django.db.models import Q

User = get_user_model()

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



def edit_genre(request):

	user = User.objects.get(id=request.user.id)
	user_genres = UserGenres.objects.filter(user=user)
	all_genres = BookCategory.objects.all()

	for i in all_genres:
		for j in user_genres:
			if str(i) == str(j):
				all_genres = all_genres.exclude(category_name=j)

	context = {		
			'user_genres': user_genres,
			'all_genres': all_genres,			
	}

	return render(request, 'accounts/new_genres.html', context)


def increase_score(instance):
	instance += 1
	return instance


def add_genres(request, id):

	user = User.objects.get(id=request.user.id)
	get_genre_object = get_object_or_404(BookCategory, id = id)
	get_genre_score = get_genre_object.get_score()

	new_score = increase_score(get_genre_score)

	get_genre_object.score = new_score
	get_genre_object.save()

	add_genre = UserGenres.objects.get_or_create(
						user = user,
						genre = get_genre_object)

	#messages.success(request, f'Your preferences have been successfully updated!')

	return redirect('accounts:edit_genres')


def add_top_genres(request, id):

	user = User.objects.get(id=request.user.id)
	get_genre_object = get_object_or_404(BookCategory, id = id)
	get_genre_score = get_genre_object.get_score()
	new_score = increase_score(get_genre_score)
	add_genre = UserGenres.objects.get_or_create(
						user = user,
						genre = get_genre_object)

	get_genre_object.score = new_score
	get_genre_object.save()

	messages.success(request, f'Your preferences have been successfully updated!')

	return redirect('accounts:genres')



def remove_genres(request, id):

	#user = User.objects.get(id=request.user.id)
	#get_genre = get_object_or_404(BookCategory, id = id)
	delete_genre = UserGenres.objects.filter(
						id=id).first()

	print(delete_genre)
	print(type(delete_genre))

	delete_genre.delete()

	#messages.success(request, f'Your preferences have been successfully updated!')

	return redirect('accounts:genres')


def remove_books(request, id):

	delete_book = UserReadList.objects.filter(id=id).first()
	delete_book.delete()

	#messages.success(request, f'Your preferences have been successfully updated!')

	return redirect('accounts:read_list')


def show_genres(request):
	user = User.objects.get(id=request.user.id)
	user_genres = UserGenres.objects.filter(user=user)

	top_genres = BookCategory.objects.all().order_by('-score') [:4]


	context = {		
			'user_genres': user_genres,
			'top_genres': top_genres,
		}
	return render(request, 'accounts/show_genres.html', context)


def show_read_list(request):
	user = User.objects.get(id=request.user.id)
	user_genres = UserGenres.objects.filter(user=user)
	read_list = UserReadList.objects.filter(user=user)
	print(read_list)
	context = {		
			'read_list': read_list,
		}
	return render(request, 'accounts/show_read_list.html', context)


def update_read_list(request):

	user = User.objects.get(id=request.user.id)
	user_genres = UserGenres.objects.filter(user=user)

	#qwe = user_genres.get_all_user_books.all()
	#print(qwe)


	if 'q' in request.GET:
		q = request.GET['q']

		if (q == ""):
			not_valid = 'Invalid search!'
			return render(request, 'accounts/update_read_list.html', {'not_valid' : not_valid, })

		else:
			books = Book.objects.filter(name__icontains=q)

			if len(books) == 0:
				not_found = 'No matching object found!'

				return render(request, 'accounts/update_read_list.html', {'not_found' : not_found, })
			
			return render(request, 'accounts/update_read_list.html', {'books' : books, })
			
	return render(request, 'accounts/update_read_list.html', {'user_genres': user_genres, })


def add_book_from_homepage(request, id):
	user = User.objects.get(id=request.user.id)
	get_book = get_object_or_404(Book, id = id)
	add_book = UserReadList.objects.get_or_create(
						user = user,
						book = get_book)

	get_book_score = get_book.get_score()
	new_score = increase_score(get_book_score)

	get_book.score = new_score
	get_book.save()

	return redirect('accounts:homepage')


def add_book_based_on_genre(request, id):

	user = User.objects.get(id=request.user.id)
	get_book = get_object_or_404(Book, id = id)
	add_book = UserReadList.objects.get_or_create(
						user = user,
						book = get_book)

	get_book_score = get_book.get_score()
	new_score = increase_score(get_book_score)

	get_book.score = new_score
	get_book.save()

	read_list = UserReadList.objects.filter(user=user)
	context = {		
		'read_list': read_list,	
		'updated_readlist': 'Your Read List has been updated!'
		}

	return render(request, 'accounts/show_read_list.html', context)
	

def show_book_by_genres(request, id):

	user = User.objects.get(id=request.user.id)
	user_genre = get_object_or_404(UserGenres, id=id)
	category = get_object_or_404(BookCategory, category_name=user_genre)
	book_by_genre = category.get_books.all()
	read_list = UserReadList.objects.filter(user=user)

	for i in read_list:
		for j in book_by_genre:
			if str(i) == str(j):
				book_by_genre = book_by_genre.exclude(name = i)

	print(type(book_by_genre))
	return render(request, 'accounts/show_book_by_genre.html', {'book_by_genre': book_by_genre,})


def check_for_empty_result(result):
	if len(result) == 0:

		not_found = 'No matching object found!'

		return not_found


def show_search_result(request):

	if request.method == 'POST':
		q = request.POST['q']

		print(q)

		if (q == ""):
			not_valid = 'Invalid search!'
			return render(request, 'accounts/show_search_results.html', {'not_valid' : not_valid, })

		else:

			name = User.objects.filter(username__icontains = q)
			by_city = Profile.objects.filter(city__icontains = q)
			books = Book.objects.filter(name__icontains=q)
			books_by_author = Book.objects.filter(author__icontains=q)
			#books_by_genre = Book.objects.filter(category__icontains=q)

			print("1", name)
			print("2", by_city)
			print("3", books)
			print("4", books_by_author)

			if len(name) == 0 and len(by_city) == 0 and len(books) == 0 and len(books_by_author) == 0:
				not_found = 'No matching object found!'
				return render(request, 'accounts/show_search_results.html', {'not_found' : not_found, })
			
			return render(request, 'accounts/show_search_results.html', 
				{
					'name' : name, 
					'by_city' : by_city, 
					'books' : books, 
					'books_by_author' : books_by_author, 
					
				})

	return render(request, 'accounts/show_search_results.html')


@login_required
def homepage_view(request):

	# v1.0 (only 10 people in suggested window (will be scaled later))


	# REMOVE SUPERUSER----------------------->

	# location - 3 (5 for now)
	# random users (for now) - 10
	#-------------------------------------
	# genres - 3
	# friend's friend - 2
	# same read_list - 2

	# FILTER : 1 (USER LOCATION, NOT IN SENT OR RECEIVED REQUESTS, NOT IN FRIENDS)
	user = User.objects.get(id=request.user.id)
	user_loc = request.user.profile.city

	sent_friend_requests = FriendRequest.objects.filter(from_user = request.user)
	rec_friend_requests = FriendRequest.objects.filter(to_user = request.user)

	#new_list = Profile.objects.filter(city = user_loc).exclude(friends = request.user.profile)
	#print("NEW ::::", new_list)

	# WORKING QUERY - 1, queries same location users which are not friends
	location_suggest = Profile.objects.filter(city = user_loc).exclude(friends = request.user.profile).exclude(user=request.user)
	#print("NEW AGAIN::::", new_list_2)

	# randomized and limited to 5 (sent to template)
	"""location_suggest_list = random.sample(list(new_list_2), min(len(list(new_list_2)), 5))"""

	# filtering requested users
	for req in sent_friend_requests:
		for item in location_suggest:
			if req.to_user== item.user:
				location_suggest = location_suggest.exclude(user = req.to_user)


	# filtering users who requested the current user
	for r_req in rec_friend_requests:
		for item in location_suggest:
			if r_req.from_user == item.user:
				location_suggest = location_suggest.exclude(user = r_req.from_user) 

	location_suggest = location_suggest.reverse() [:4]
				


#-------------------------------------------------------------------------------------------------
	
	# FILTER : 2 (NOT IN LOCATION, FRIENDS, SENT OR RECEIVED REQUESTS)

	
	not_friends = Profile.objects.exclude(friends = request.user.profile)
	not_friends_suggest_list = not_friends.exclude(user = request.user)

	#NOT friends NOT same location
	not_friend_neither_location = not_friends_suggest_list.exclude(city=user_loc)

	# randomized and limited to 10 (sent to template)
	"""not_friend_neither_location_list = random.sample(list(not_friend_neither_location), 
		min(len(list(not_friend_neither_location)), 10))"""



	# filtering requested users
	for req in sent_friend_requests:
		for item in not_friend_neither_location:
			if req.to_user== item.user:
				#print(req.to_user.id)
				not_friend_neither_location = not_friend_neither_location.exclude(user = req.to_user)

	# filtering users who requested the current user
	for r_req in rec_friend_requests:
		for item in not_friend_neither_location:
			if r_req.from_user == item.user:
				#print(r_req.from_user.id)
				not_friend_neither_location = not_friend_neither_location.exclude(user = r_req.from_user)
				#print(not_friend_neither_location)

	not_friend_neither_location = not_friend_neither_location.reverse() [:4]
	#print("111111111111111111111111111", not_friend_neither_location)

	#print(type(not_friend_neither_location))




#-----------------------------------PERFECTLY WORKING ----------------------------------------------



	# posts by all the users except the current users

	#posts = Post.objects.all().order_by('-date_posted').exclude(user_name = request.user)
	posts = Post.objects.all().order_by('-date_posted')





	# user genres
	#current_user_genres = request.user.profile.genres

	# user genres list form
	#current_user_genres_list = list(current_user_genres.split("  "))
	# sorted genres list
	#sorted_genre_list = sorted(current_user_genres_list)

	"""length_sorted_genre = len(sorted_genre_list)


	if length_sorted_genre >= 2:
		gen_list = Profile.objects.filter(Q(genres = sorted_genre_list[0]) | Q(genres = sorted_genre_list[1]))

		gen_list2 = Profile.objects.filter(genres = current_user_genres)
		print(gen_list)"""

		# suggested reads

	sugg_books = Book.objects.all().order_by('-score')
	read_list = UserReadList.objects.filter(user=user)

	for i in sugg_books:
		for j in read_list:
			if str(i) == str(j):
				sugg_books = sugg_books.exclude(name=j)

	sugg_books = sugg_books [:8]
	#print(sugg_books)

	context = {
			
			'sent_friend_requests': sent_friend_requests,
			'rec_friend_requests' : rec_friend_requests,
			'location_suggest' : location_suggest,
			'not_friend_neither_location' : not_friend_neither_location,
			'posts' : posts,
			'sugg_books': sugg_books,

	}

	print(location_suggest)

	return render(request, 'accounts/test_homepage.html', context)


@login_required
def read_list(request):
	pass


@login_required
def edit_profile_view(request):
	# return HttpResponse(slug)
	rec_friend_requests = FriendRequest.objects.filter(to_user = request.user)

	if request.method == "POST":

		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
		i_form = ProfileImageUpdateForm(request.POST,request.FILES,  instance=request.user)


		if u_form.is_valid() and p_form.is_valid() and i_form.is_valid():
			u_form.save()
			p_form.save()
			i_form.save()
			messages.success(request, f'Your profile has been successfully updated!')
			return redirect('accounts:edit_profile')

		else:
			messages.success(request, f'Fill all the fields!')

	else:

		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
		i_form = ProfileImageUpdateForm(instance=request.user.profile)

	context = {
		'u_form' : u_form,
		'p_form' : p_form,
		'i_form' : i_form,
		'rec_friend_requests' : rec_friend_requests,

	}

	return render(request, 'accounts/edit_profile.html', context)



#------------------------------- currently working on ----------

# users_list view used in the my_profile view

@login_required
def users_list(request):

	rec_friend_requests = FriendRequest.objects.filter(to_user = request.user)

	
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
			'rec_friend_requests' : rec_friend_requests,
			'sent' : sent_to
	}

	return render(request, "accounts/users_list.html", context)



@login_required
def profile_view(request, slug):

	rec_friend_requests = FriendRequest.objects.filter(to_user = request.user)


	p = Profile.objects.filter(slug=slug).first()
	u = p.user
	print(u)
	print(type(u))

	user_genres = UserGenres.objects.filter(user=u)
	user_read_list = UserReadList.objects.filter(user=u)



	sent_friend_requests = FriendRequest.objects.filter(from_user=p.user)
	rec_friend_requests = FriendRequest.objects.filter(to_user=p.user)
	user_posts = Post.objects.filter(user_name=u)

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
	
	context = {
		'u': u,
		'rec_friend_requests' : rec_friend_requests,
		'button_status': button_status,
		'friends_list': friends,
		'sent_friend_requests': sent_friend_requests,
		'rec_friend_requests': rec_friend_requests,
		'post_count': user_posts.count,
		'user_genres': user_genres,
		'user_read_list': user_read_list,
	 
	}

	return render(request, "accounts/profile.html", context)


def friend_list(request):

	p = request.user.profile
	you = p.user
	sent_friend_requests = FriendRequest.objects.filter(from_user = you)
	rec_friend_requests = FriendRequest.objects.filter(to_user = you)

	friends = p.friends.all()
	context = { 
		'sent_friend_requests': sent_friend_requests,
		'rec_friend_requests': rec_friend_requests,
		'friends' : friends
	}
	return render (request, "accounts/friends_list.html", context)


@login_required
def send_friend_request(request, id):
	user = get_object_or_404 (User, id = id)
	frequest , created = FriendRequest.objects.get_or_create(
						from_user = request.user,
						to_user = user )

	#return HttpResponseRedirect('/accounts/homepage/')
	return redirect('accounts:homepage')

#NEWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW 20/03-------------------------------------------
@login_required
def send_friend_request_from_homepage(request, id):
	user = get_object_or_404 (User, id = id)
	frequest , created = FriendRequest.objects.get_or_create(
						from_user = request.user,
						to_user = user )

	#return HttpResponseRedirect('/accounts/homepage/')
	return redirect('accounts:homepage')
	


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
	#return HttpResponseRedirect('/accounts/friend_list/')
		

	messages.success(request, " {} has been added to friends list!".format(user_2.username))

	return redirect('accounts:friend_list')


@login_required
def delete_friend_request(request, id):
	from_user = get_object_or_404(User, id = id)
	frequest = FriendRequest.objects.filter(from_user = from_user, to_user = request.user).first()
	frequest.delete()
	return redirect('accounts:friend_list')

# 22/03 --------------------------------------------------------------------------

@login_required
def delete_friend_request_from_friend_list(request, id):
	to_user = get_object_or_404(User, id = id)
	frequest = FriendRequest.objects.filter(from_user = request.user, to_user = to_user).first()
	frequest.delete()
	return redirect('accounts:friend_list')

#---------------------------------------------------------------------------------------



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

	#return HttpResponseRedirect('/accounts/homepage/')
	return redirect('accounts:homepage')




# renders the logged in user's profile

@login_required
def my_profile(request):

	p = request.user.profile
	you = p.user
	sent_friend_requests = FriendRequest.objects.filter(from_user = you)
	rec_friend_requests = FriendRequest.objects.filter(to_user = you)

	user_posts = Post.objects.filter(user_name = you)
	friends = p.friends.all()

		# is this user our friend
	button_status = 'none'
	if p not in request.user.profile.friends.all():
		button_status = 'not_friend'

		# if we have sent him a friend request
		if len(FriendRequest.objects.filter(
			from_user=request.user).filter(to_user=you)) == 1:
				button_status = 'friend_request_sent'

		if len(FriendRequest.objects.filter(
			from_user=p.user).filter(to_user=request.user)) == 1:
				button_status = 'friend_request_received'

	context = {
		'u': you,
		'button_status': button_status,
		'friends_list': friends,
		'sent_friend_requests': sent_friend_requests,
		'rec_friend_requests': rec_friend_requests,
		'post_count': user_posts.count
	}

	return render(request, "accounts/my_profile.html", context)



def notification_view(request):

	rec_friend_requests = FriendRequest.objects.filter(to_user = request.user)

	p = request.user.profile


	context = {

			'rec_friend_requests': rec_friend_requests,

	}


	return render(request, "accounts/notifications.html", context)
