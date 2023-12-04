from django.db import migrations
from games.models import (GameStatistics,
                          Country,
                          Producer,
                          Genre,
                          Game)
import csv
import datetime


def load_initial_data(app, schema_editor):
    """ Odczyt pliku csv """
    with open('games/migrations/games.csv', 'r', encoding='windows-1250') as games_data:

        games_data.readline()
        games_data_content = csv.reader(games_data, delimiter=';')

        for row in games_data_content:

            statistics = GameStatistics(vote_average=float(row[5].replace(',', '.')),
                                        vote_count=int(row[6]))
            statistics.save()

            country, created = Country.objects.get_or_create(country=row[7])

            producer, created = Producer.objects.get_or_create(producer=row[8])

            genres = [Genre.objects.get_or_create(genre=genre.strip())[0] for genre in row[9].split(',')]

            game = Game(title=row[1],
                        cycle=row[2],
                        release_date=datetime.datetime.strptime(row[3], '%d.%m.%Y'),
                        depiction=row[4],
                        statistics=statistics,
                        country=country,
                        producer=producer)

            game.save()

            game.genres.set(genres)


class Migration(migrations.Migration):
    dependencies = [
        ('games', '0001_initial')
    ]

    operations = [
        migrations.RunPython(load_initial_data)
    ]