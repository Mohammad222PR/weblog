from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from account.forms import LoginForm, SingupForm, EditAccountForm


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
                next_page = request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('home:home')

    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def Register(request):
    if request.user.is_authenticated:
        return redirect('home:home')
    if request.method == "POST":
        form = SingupForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['password1'], cd['password2'])
            user = authenticate(request, username=cd['username'], password=cd['password1'])
            login(request, user)
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect('home:home')

    else:
        form = SingupForm()
    return render(request, 'account/register.html', {'form': form})


def Logout(request):
    logout(request)
    next_page = request.GET.get('next')
    if next_page:
        return redirect(next_page)

    return redirect('home:home')


def EditAccountView(request):
    if request.user.is_authenticated:
        return redirect('home:home')
    user = request.user
    form = EditAccountForm(instance=user)
    if request.method == 'POST':
        form = EditAccountForm(instance=user, data=request.POST)
        if form.is_valid():
            edit = form.save()
            edit.user = request.user
            edit.save()
            return redirect('account:edit_account')
    return render(request, 'account/edit_account.html', {'form': form})
