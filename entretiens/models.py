from django.db import models

from django.core.validators import MinValueValidator

class Entretien(models.Model):
    numero = models.CharField(max_length=20, primary_key=True)
    intervenant = models.ForeignKey(
        "intervenants.Intervenant", on_delete=models.PROTECT, related_name="entretiens"
    )
    materiel = models.ForeignKey(
        "materiel.Materiel", on_delete=models.PROTECT, related_name="entretiens"
    )
    date_intervention = models.DateField()
    nombre_heures = models.DecimalField(
        max_digits=5, decimal_places=1,
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return f"{self.numero} - {self.materiel} ({self.date_intervention})"
