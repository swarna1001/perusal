from django.shortcuts import render
from django.http import HttpResponse


def basic_home_view(request):
	
	#return render(request, 'basic_home.html')

	return render(request, 'basic_home.html')

