from django.db import migrations
from games.models import (Game,
                          GameStatistics,
                          Country,
                          Producer,
                          Genre)
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

            country = Country(country=row[7])

            producer = Producer(producer=row[8])

            game = Game(title=row[1],
                        cycle=row[2],
                        release_date=datetime.datetime.strptime(row[3], '%d.%m.%Y'),
                        depiction=row[4],
                        genres=(row[9]))

            statistics.save()
            country.save()
            producer.save()

            game.statistics = statistics
            game.country = country
            game.producer = producer

            game.save()


class Migration(migrations.Migration):
    dependencies = [
        ('games', '0001_initial')
    ]

    operations = [
        migrations.RunPython(load_initial_data)
    ]
