from django.shortcuts import render, redirect, get_object_or_404
from .models import Materiel
from django.db.models import Q
from .forms import MaterielForm


def liste_materiels(request):
    q = request.GET.get('q', "")

    materiels = Materiel.objects.all()

    if q:
        materiels = materiels.filter(
            Q(numero__icontains=q) |
            Q(designation__icontains=q) |
            Q(marque__icontains=q) |
            Q(etat__icontains=q)
        )

    return render(
        request,
        'materiel/materiel.html',
        {'materiels': materiels}
    )



def ajouter_materiel(request):
    if request.method == 'POST':
        form = MaterielForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('liste_materiels')
    else:
        form = MaterielForm()

    return render(request, 'materiel/ajouter.html', {'form': form})
            
      
def supprimer_materiel(request, numero):
    materiel = get_object_or_404(Materiel, numero=numero)

    if request.method == 'POST':
        materiel.delete()
        return redirect('liste_materiels')

    return render(
        request,
        'materiel/supprimer.html',
        {'materiel': materiel}
    )

def modifier_materiel(request, numero):
    materiel = get_object_or_404(Materiel, numero=numero)

    if request.method == 'POST':
        ancien_numero = materiel.numero

        form = MaterielForm(request.POST, instance=materiel)

        if form.is_valid():
            donnees = form.cleaned_data

            Materiel.objects.filter(numero=ancien_numero).update(
                numero=donnees['numero'],
                designation=donnees['designation'],
                marque=donnees['marque'],
                etat=donnees['etat']
            )

            return redirect('liste_materiels')

    else:
        form = MaterielForm(instance=materiel)

    return render(request, 'materiel/modifier.html', {'form': form})