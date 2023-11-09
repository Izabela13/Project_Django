from django.urls import path
from . import views
from . import models


urlpatterns = [
    path('', views.start, name='start')
]
