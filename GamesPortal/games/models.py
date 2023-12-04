from django.db import models


# Create your models here.


""" Modele tabel dla gier """


class GameStatistics(models.Model):
    """ Średnia ocena i liczba ocen gier """
    vote_average = models.DecimalField(max_digits=3,
                                       decimal_places=1,
                                       blank=True,
                                       default=0)
    vote_count = models.IntegerField(blank=True,
                                     default=0)


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
                             blank=True)
    release_date = models.DateField(blank=True)
    depiction = models.TextField(blank=True)
    statistics = models.OneToOneField(GameStatistics,
                                      blank=True,
                                      on_delete=models.CASCADE)
    country = models.ForeignKey(Country,
                                blank=True,
                                on_delete=models.SET(''),
                                default='')
    producer = models.ForeignKey(Producer,
                                 blank=True,
                                 on_delete=models.SET(''),
                                 default='')
    genres = models.ManyToManyField(Genre)

    def __str__(self) -> str:
        return f'Nazwa gry: {self.title}'
