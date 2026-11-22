from django.urls import path
from . import views

urlpatterns = [
    path('rapports/', views.liste_rapports, name='liste_rapports'),
    path(
        'exporter-pdf/',
        views.exporter_rapport_pdf,
        name='exporter_rapport_pdf'
    ),
]
