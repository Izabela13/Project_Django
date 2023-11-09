from django.db import migrations
from games.models import (Game,
                          GameStatistics,
                          Country,
                          Producer,
                          Genre,
                          GamesGenres)
import csv
import datetime


def load_initial_data(app, schema_editor):
    """ Odczyt pliku csv """
    with (open('games/migrations/games.csv', 'r', encoding='windows-1250') as main_data,
          open('games/migrations/genres.csv', 'r', encoding='utf-8') as genre_data,
          open('games/migrations/games_genres.csv', 'r', encoding='windows-1250') as games_genres_data):

        main_data.readline()
        main_data_content = csv.reader(main_data, delimiter=';')

        for row in main_data_content:
            statistics = GameStatistics(vote_average=float(row[5].replace(',', '.')),
                                        vote_count=int(row[6]))

            country = Country(country=row[7])

            producer = Producer(producer=row[8])

            game = Game(title=row[1],
                        cycle=row[2],
                        release_date=datetime.datetime.strptime(row[3], '%d.%m.%Y'),
                        depiction=row[4],
                        genres=row[9])

            statistics.save()
            country.save()
            producer.save()

            game.statistics = statistics
            game.country = country
            game.producer = producer

            game.save()

        ######################################################################################

        genre_data.readline()
        genre_data_content = csv.reader(genre_data, delimiter=';')

        for row in genre_data_content:
            genre = Genre(genre=row[1])

        genre.save()

        ######################################################################################

        games_genres_data.readline()
        games_genres_content = csv.reader(games_genres_data, delimiter=';')

        for row in games_genres_content:
            game_genres = GamesGenres(game_id=row[0],
                                      title=row[1],
                                      genre_id=row[2],
                                      genre=row[3])

        game_genres.save()

################################################################################################


class Migration(migrations.Migration):
    dependencies = [
        ('games', '0001_initial')
    ]

    operations = [
        migrations.RunPython(load_initial_data)
    ]
