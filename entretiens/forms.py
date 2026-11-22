from django import forms
from .models import Entretien


class EntretienForm(forms.ModelForm):

    class Meta:
        model = Entretien
        fields = [
            'numero',
            'intervenant',
            'materiel',
            'date_intervention',
            'nombre_heures',
        ]

        labels = {
            'numero': "Numéro de l'entretien",
            'intervenant': 'Intervenant',
            'materiel': 'Matériel',
            'date_intervention': "Date d'intervention",
            'nombre_heures': "Nombre d'heures",
        }

        widgets = {
            'numero': forms.TextInput(attrs={
                'class': 'input w-full',
                'placeholder': 'Ex : ENT001'
            }),

            'intervenant': forms.Select(attrs={
                'class': 'input w-full',
            }),

            'materiel': forms.Select(attrs={
                'class': 'input w-full',
            }),

            'date_intervention': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'input w-full',
                    'type': 'date',
                },
            ),

            'nombre_heures': forms.NumberInput(attrs={
                'class': 'input w-full',
                'placeholder': "Entrez le nombre d'heures",
                'step': '0.5',
                'min': '0',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Listes déroulantes lisibles : "INT001 - Nom" / "MAT001 - Ordinateur"
        self.fields['intervenant'].empty_label = "Choisir un intervenant"
        self.fields['intervenant'].label_from_instance = (
            lambda i: f"{i.numero} - {i.nom}"
        )

        self.fields['materiel'].empty_label = "Choisir un matériel"
        self.fields['materiel'].label_from_instance = (
            lambda m: f"{m.numero} - {m.designation}"
        )

        # En modification, le numéro (clé primaire) ne doit pas changer :
        # sinon Django créerait un second entretien au lieu de modifier l'ancien.
        if self.instance and self.instance.pk:
            self.fields['numero'].disabled = True