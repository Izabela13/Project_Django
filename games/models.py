from django.db import models
from django.core.validators import MinLengthValidator


# Create your models here.


""" Modele tabel """


class GameStatistics(models.Model):
    """ Średnia ocena i liczba ocen gier """
    vote_average = models.DecimalField(max_digits=3,
                                       decimal_places=1,
                                       null=True)
    vote_count = models.IntegerField(null=True, default=0)


class Country(models.Model):
    """ Kraj powstania gry """
    country = models.CharField(max_length=60,
                               verbose_name='Kraj powstania gry',
                               unique=True)


class Producer(models.Model):
    """ Producent (główny) gry """
    producer = models.CharField(max_length=35,
                                verbose_name='Producent (główny) gry',
                                unique=True)


class Genre(models.Model):
    """ Gatunki gier """
    genre = models.TextField(unique=True)


class Game(models.Model):
    """ Gry """
    title = models.CharField(max_length=1000)
    cycle = models.CharField(max_length=30,
                             null=True)
    release_date = models.DateField(null=True)
    depiction = models.TextField(null=True)
    statistics = models.OneToOneField(GameStatistics,
                                      null=True,
                                      on_delete=models.SET_NULL)
    country = models.ForeignKey(Country,
                                null=True,
                                on_delete=models.SET_NULL,
                                default='null')
    producer = models.ForeignKey(Producer,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 default='null')
    genres = models.TextField(null=True)

    def __str__(self) -> str:
        return f'Nazwa gry: {self.title}'


class GamesGenres(models.Model):
    """ Połączenie gier i ich gatunków """
    game_id = models.CharField(max_length=10)
    title = models.CharField(max_length=1000)
    genre_id = models.CharField(max_length=3)
    genre = models.TextField()
