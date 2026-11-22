from django.shortcuts import render, redirect, get_object_or_404
from .models import Intervenant
from django.db.models import Q
from .forms import IntervenantForm

def liste_intervenants(request):
    q = request.GET.get('q', "")

    intervenants = Intervenant.objects.all()

    if q:
        intervenants = intervenants.filter(
            Q(numero__icontains=q) |
            Q(nom__icontains=q)
        )

    return render(
        request,
        'intervenant/intervenant.html',
        {
            'intervenants': intervenants,
            'q': q
        }
    )

def ajouter_intervenant(request):
    if request.method == 'POST':
        form = IntervenantForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('liste_intervenants')
    else:
        form = IntervenantForm()

    return render(
        request,
        'intervenant/ajouter_inter.html',
        {'form': form}
    )


def supprimer_intervenant(request, numero):
    intervenant = get_object_or_404(Intervenant, numero=numero)

    if request.method == 'POST':
        intervenant.delete()
        return redirect('liste_intervenants')

    return render(
        request,
        'intervenant/supprimer_inter.html',
        {'intervenant': intervenant}
    )

def modifier_intervenant(request, numero):
    intervenant = get_object_or_404(Intervenant, numero=numero  )

    if request.method == 'POST':
        ancien_numero = intervenant.numero

        form = IntervenantForm(request.POST, instance=intervenant)

        if form.is_valid():
            donnees = form.cleaned_data

            Intervenant.objects.filter(numero=ancien_numero).update(
                numero=donnees['numero'],
                nom=donnees['nom'],
                taux_horaire=donnees['taux_horaire']
            )

            return redirect('liste_intervenants')

    else:
        form = IntervenantForm(instance=intervenant)

    return render(
        request,
        'intervenant/modifier_inter.html',
        {'form': form}
    )