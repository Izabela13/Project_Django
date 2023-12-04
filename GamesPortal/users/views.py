from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm


# Create your views here.
def register(request):
    storage = messages.get_messages(request)
    storage.used = True

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            messages.success(request, 'Rejestracja zakończona pomyślnie.')
            return redirect('logging')  # przekierowanie do strony logowania po poprawnej rejestracji
    else:
        register_form = RegisterForm()

    return render(request, 'users/register.html', {'register_form': register_form})


def logon(request):
    storage = messages.get_messages(request)  # Czyszczenie komunikatów
    storage.used = True

    if request.method == 'POST':
        login_form = LoginForm(request, request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, 'Jesteś zalogowany :) .')
            return redirect('logging')

    else:
        login_form = LoginForm()

    if request.method == 'POST' and 'clean_button' in request.POST:
        login_form = LoginForm()

    return render(request, 'users/login.html', {'login_form': login_form})


def log_out(request):
    logout(request)
    messages.success(request, 'Pomyślne wylogowanie.')
    return redirect('logging')


def clean_form(request):
    if request.method == 'POST':
        login_form = LoginForm()
        return render(request, 'users/login.html', {'login_form': login_form})
    else:
        return redirect('logging')  # Przekierowanie na stronę logowania
