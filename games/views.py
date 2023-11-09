from django.shortcuts import render
from . import models


# Create your views here.
def start(request):
    welcome = "WELCOME TO THE GAMES"
    return render(request, 'games/start_page.html', {
        'welcome_writing': welcome
    })
