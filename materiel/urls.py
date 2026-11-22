from django.urls import path
from . import views

urlpatterns = [
    path('materiels/', views.liste_materiels, name='liste_materiels'),
    path('materiels/ajouter/', views.ajouter_materiel, name='ajouter_materiel'),
    path('modifier/<str:numero>/', views.modifier_materiel, name='modifier_materiel'),
    path('supprimer/<str:numero>/', views.supprimer_materiel, name='supprimer_materiel'),
]
