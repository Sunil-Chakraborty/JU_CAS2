from django.shortcuts import render, redirect
from account.models import Account
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User


def temp(request):
	context = {}
	return render(request, "personal/temp1.html", context)



def dashboard(request):
	context = {}
	return render(request, "personal/dashboard.html", context)

def home_proj(request):
	context = {}
	return render(request, "personal/home.html", context)


def home_screen_view(request):
	context = {}
	return render(request, "personal/home2.html", context)

