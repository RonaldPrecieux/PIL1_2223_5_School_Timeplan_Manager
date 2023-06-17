from django.shortcuts import render, redirect
from showtimeplan.models import User

def formreg(request):
    return render(request, 'showtimeplan/exemple.html')

def insertuser(request):
    vu_nom=request.POST['Nom']
    vu_prenom = request.POST['Prenom'] #Les élements entre crochets sont les "name" des input dans le template. Les vu_ créées sont des variables qui récupèrent l'attribut "name du template.
    vu_email = request.POST ['Email']
    vu_phone = request.POST['Phone']
    vu_mot_de_passe = request.POST['Mot_de_passe']
    vu_confirmer_mot_de_passe = request.POST['Mot_de_passe_confirm']
    us=User(nom = vu_nom, prenom = vu_prenom, email = vu_email, numero_telephone =vu_phone, mot_de_passe = vu_mot_de_passe, confirmer_mot_de_passe = vu_confirmer_mot_de_passe)
    #Cette ligne sert à lier le champ dans la base de données(modèle) aux variables vu_
    us.save()
    prenom_user = us.prenom
    return redirect("bienvenue", prenom = prenom_user)

def index(request):
    return render(request, "showtimeplan/index.html")

def login(request):
    return render(request, "showtimeplan/login.html")

def register(request):
    return render(request, "showtimeplan/register.html")

def bienvenue(request, prenom):
    return render(request, 'showtimeplan/bienvenue.html', {'prenom' : prenom})