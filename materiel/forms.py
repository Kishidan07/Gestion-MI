from django import forms
from .models import Materiel

class MaterielForm(forms.ModelForm):

    class Meta:
        model = Materiel
        fields = ['numero', 'designation', 'marque', 'etat']

        widgets = {
            'numero': forms.TextInput(attrs={
                'class': 'input w-full',
                'placeholder': 'Ex : MAT001'

            }),

            'designation': forms.TextInput(attrs={
                'class': 'input w-full',
                'placeholder': 'Entrez la désignation du matériel'
            }),

            'marque': forms.TextInput(attrs={
                'class': 'input w-full',
                'placeholder': 'Entrez la marque du matériel'
            }),

            'etat': forms.Select(attrs={
                'class': 'input w-full'
            }),
        }