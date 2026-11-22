from django.db import models


class Intervenant(models.Model):
    numero = models.CharField(max_length=20, primary_key=True)
    nom = models.CharField(max_length=150)
    taux_horaire = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nom