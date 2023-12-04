from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('logging', views.logon, name='logging'),
    path('clean_form', views.clean_form, name='clean_form'),
    path('logout', views.log_out, name='logout')
]
