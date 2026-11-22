from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inscription, name='inscription'),
    path('acceuil', views.acceuil, name='acceuil'),
    path('connexion/', views.connexion, name='connexion'),
    ]
