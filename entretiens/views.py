from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Entretien
from .forms import EntretienForm


def liste_entretiens(request):
    q = request.GET.get('q', "")

    entretiens = Entretien.objects.select_related(
        'intervenant', 'materiel'
    ).order_by('-date_intervention')

    if q:
        entretiens = entretiens.filter(
            Q(numero__icontains=q) |
            Q(intervenant__numero__icontains=q) |
            Q(intervenant__nom__icontains=q) |
            Q(materiel__numero__icontains=q) |
            Q(materiel__designation__icontains=q)
        )

    return render(
        request,
        'entretien/entretien.html',
        {
            'entretiens': entretiens,
            'q': q
        }
    )


def ajouter_entretien(request):
    if request.method == 'POST':
        form = EntretienForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('liste_entretiens')
    else:
        form = EntretienForm()

    return render(
        request,
        'entretien/ajouter_ent.html',
        {'form': form}
    )


def modifier_entretien(request, numero):
    entretien = get_object_or_404(Entretien, numero=numero)

    if request.method == 'POST':
        form = EntretienForm(request.POST, instance=entretien)

        if form.is_valid():
            form.save()
            return redirect('liste_entretiens')
    else:
        form = EntretienForm(instance=entretien)

    return render(
        request,
        'entretien/modifier_ent.html',
        {'form': form, 'entretien': entretien}
    )


def supprimer_entretien(request, numero):
    entretien = get_object_or_404(Entretien, numero=numero)

    if request.method == 'POST':
        entretien.delete()
        return redirect('liste_entretiens')

    return render(
        request,
        'entretien/supprimer_ent.html',
        {'entretien': entretien}
    )

