from django.db import models

class Materiel(models.Model):
    numero = models.CharField(max_length=100, primary_key=True)
    designation = models.CharField(max_length=150)
    marque = models.CharField(max_length=100)
    etat = models.CharField(
        max_length=100,
        choices=[
            ('En panne', 'En panne'),
            ('En maintenance', 'En maintenance'),
            ('En bon état', 'En bon état'),
        ],
        default='En bon état'
    )

    def __str__(self):
        return self.numero