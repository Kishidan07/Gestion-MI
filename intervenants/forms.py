from django import forms
from .models import Intervenant


class IntervenantForm(forms.ModelForm):

    class Meta:
        model = Intervenant
        fields = ['numero', 'nom', 'taux_horaire']

        widgets = {
            'numero': forms.TextInput(attrs={
                'class': 'input w-full',
                'placeholder': 'Ex : INT001'
            }),

            'nom': forms.TextInput(attrs={
                'class': 'input w-full',
                'placeholder': "Entrez le nom de l'intervenant"
            }),

            'taux_horaire': forms.NumberInput(attrs={
                'class': 'input w-full',
                'placeholder': 'Entrez le taux horaire',
                'step': '0.01'
            }),
        }