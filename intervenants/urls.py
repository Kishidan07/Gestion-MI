from django.urls import path
from . import views

urlpatterns = [
    path('intervenants/', views.liste_intervenants, name='liste_intervenants'),
    path('intervenants/ajouter/', views.ajouter_intervenant, name='ajouter_intervenant'),
    path('modifier/<str:numero>/', views.modifier_intervenant, name='modifier_intervenant'),
    path('supprimer/<str:numero>/', views.supprimer_intervenant, name='supprimer_intervenant'),
]