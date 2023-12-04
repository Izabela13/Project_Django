from django.urls import path
from . import views
from . import models


urlpatterns = [
    path('', views.start, name='start_page'),
    path('all_games', views.all_games, name='all_games'),
    path('<int:id>', views.game_details, name='game_details'),
    path('search_game', views.search_game, name='search_game'),
    path('ranking', views.top, name='the_best')
]
