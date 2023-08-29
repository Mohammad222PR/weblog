from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from account.forms import LoginForm, SingupForm


# Create your views here.


def Login(request):
    if request.user.is_authenticated:
        return redirect('home:home')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('home:home')
    return render(request, 'account/login.html')


def Register(request):
    context = {"errors": []}
    if request.user.is_authenticated:
        return redirect('home:home')
    if request.method == "POST":
        form = SingupForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['password1'], cd['password2'])
            user = authenticate(request, username=cd['username'], password=cd['password1'])
            login(request, user)
            return redirect('home:home')
    return render(request, 'account/register.html', {})


def Logout(request):
    logout(request)
    return redirect('home:home')
