from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from . import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import GameSearchForm


# Create your views here.
def start(request):
    """ strona startowa """
    welcome = "WELCOME TO THE GAMES"
    return render(request, 'games/start_page.html', {
        'welcome_writing': welcome})


def all_games(request):
    """ widok z listą wszystkich dostępnych gier ujętą w tabelę z paginacją """
    all_games_list = models.Game.objects.all().order_by('title')

    paginator = Paginator(all_games_list, 10)
    page = request.GET.get('page')

    try:
        all_games_list = paginator.page(page)
    except PageNotAnInteger:
        all_games_list = paginator.page(1)
    except EmptyPage:
        all_games_list = paginator.page(paginator.num_pages)

    return render(request, 'games/all_games.html', {
        'all_games_list': all_games_list})


def game_details(request, id):
    """ widok ze szczegółami danej gry """
    try:
        show_game = get_object_or_404(models.Game, pk=id)
        stored_games = models.Game.objects.all().order_by('title')

        current_game_index = 0
        for i, g in enumerate(stored_games):
            if g.id == show_game.id:
                current_game_index = i
                break

        is_first_game = current_game_index == 0
        is_last_game = current_game_index == len(stored_games) - 1

        next_game = stored_games[current_game_index + 1] if not is_last_game else None
        prev_game = stored_games[current_game_index - 1] if not is_first_game else None

        paginator_page = request.GET.get('page')

        return render(request, 'games/game_details.html', {
            'game_details': show_game,
            'next_game': next_game,
            'prev_game': prev_game,
            'paginator_page': paginator_page})
    except Http404:
        return render(request, 'games/game_not_found.html')


def search_game(request):
    """ wyszukiwanie gry (gier) """
    form = GameSearchForm(request.GET)
    result = []

    if form.is_valid():
        query = form.cleaned_data['search_query']

        if query:
            if len(query) == 1:
                result = models.Game.objects.filter(title__istartswith=query)
            else:
                result = models.Game.objects.filter(title__icontains=query)

    return render(request, 'games/search_game.html', {
        'form': form,
        'result': result})


def top(request):
    the_best_games = models.Game.objects.order_by('-statistics__vote_average')[:10]
    return render(request, 'games/ranking.html', {
        'the_best_games': the_best_games})
