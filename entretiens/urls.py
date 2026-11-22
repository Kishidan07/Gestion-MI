from django.urls import path
from . import views

urlpatterns = [
    path('entretiens/', views.liste_entretiens, name='liste_entretiens'),
    path('entretiens/ajouter/', views.ajouter_entretien, name='ajouter_entretien'),
    path('entretiens/modifier/<str:numero>/', views.modifier_entretien, name='modifier_entretien'),
    path('entretiens/supprimer/<str:numero>/', views.supprimer_entretien, name='supprimer_entretien'),
]