from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from account.forms import LoginForm


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
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            context['errors'].append('password not mach')
            return render(request, 'account/register.html', context)

        User.objects.create_user(username=username, email=email, password=password1)
        user = authenticate(request, username=username, password=password1)
        login(request, user)
        return redirect('home:home')

    return render(request, 'account/register.html', {})


def Logout(request):
    logout(request)
    return redirect('home:home')
