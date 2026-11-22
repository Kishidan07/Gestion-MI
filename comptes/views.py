from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from materiel.models import Materiel


def inscription(request):

    if request.method == 'POST':

        nom = request.POST.get('nom', '').strip()
        mdp = request.POST.get('mdp')
        mdp_confirm = request.POST.get('mdp2')

        if mdp != mdp_confirm:
            messages.error(request, 'Les mots de passe ne correspondent pas.')
            return redirect('inscription')

        if User.objects.filter(username=nom).exists():
            messages.error(request, "Ce nom d'utilisateur est déjà utilisé.")
            return redirect('inscription')

        utilisateur = User.objects.create_user(
            username=nom,
            password=mdp
        )

        login(request, utilisateur)

        messages.success(request, 'Inscription réussie !')

        return redirect('acceuil')

    return render(request, 'pages/inscription.html')


def connexion(request):
    
    if request.method == 'POST':
        nom = request.POST.get('nom')
        mdp = request.POST.get('mdp')

        utilisateur = authenticate(request, 
                        username=nom, 
                        password=mdp)

        if utilisateur is not None:
            login(request, utilisateur)
            messages.success(request, 'Connexion réussie !')
            return redirect('acceuil')
        else:
            messages.error(request, 'Nom d’utilisateur ou mot de passe incorrect.')
           
            return redirect('connexion')
    
    return render(request, 'pages/connexion.html')


def acceuil(request):
    from materiel.models import Materiel


def acceuil(request):

    materiels = Materiel.objects.all()

    stats = {
        'total': materiels.count(),

        'en_service': materiels.filter(etat='En bon état').count(),

        'maintenance': materiels.filter(etat='En maintenance').count(),

        'en_panne': materiels.filter(etat='En panne').count(),
    }

    return render(request, 'pages/acceuil.html', {
        'stats': stats
    })
    
