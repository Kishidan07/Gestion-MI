from django.contrib import admin
from django.contrib.admin import views
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('comptes.urls')),
    path('materiel/', include('materiel.urls')),
    path('intervenant/', include('intervenants.urls')),
    path('entretien/', include('entretiens.urls')),
    path('rapports/', include('rapports.urls')),
    ]
