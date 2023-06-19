from django.shortcuts import render, redirect
from showtimeplan.forms import UserForm
from showtimeplan.models import User
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.hashers import make_password
import random


def insertuser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'Email déjà utilisé')
                
            form.save()
            prenom_user = form.cleaned_data['prenom']
            return redirect("bienvenue", prenom=prenom_user)
    else:
        form = UserForm()
        
    context = {'form': form}
    return render(request, 'showtimeplan/register.html', context)

def index(request):
    return render(request, "showtimeplan/index.html")



def login(request):     #Vue d'identification. Elle vous identifie à partie de votre mot de passe et votre email et vous connecte à votre compte
    if request.method == 'POST':
        email = request.POST.get('email')
        mot_de_passe = request.POST.get('mot_de_passe')
        try:
            user = User.objects.get(email=email, mot_de_passe=mot_de_passe) #Cette ligne permet de vérifier si l'utilisateur existe dans la base de données. Elle lance une recherche de l'email et du mot de passe qu'il a entré dans le champ de recherche dans la base de données
            return redirect('bienvenue_connexion', prenom=user.prenom)
        except User.DoesNotExist:
            context = {
            'error_message': 'Email ou mot de passe incorrect. Réessayez !',
            'email_value': email,  
            'password_value': mot_de_passe,
            }
            return render(request, 'showtimeplan/login.html', context)

    return render(request, 'showtimeplan/login.html')




def register(request):
    return render(request, "showtimeplan/register.html")

def bienvenue(request, prenom):
    return render(request, 'showtimeplan/bienvenue.html', {'prenom' : prenom})

def bienvenue_connexion(request, prenom):
    return render(request, 'showtimeplan/bienvenue_connexion.html', {'prenom' : prenom})


def mot_de_passe_oublie(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            code = (random.randint(100000, 999999))
            user.reset_code = code
            user.save()
            
            # Envoyer l'email de réinitialisation
            subject = 'Réinitialisation du mot de passe'
            message = f'Votre code de réinitialisation du mot de passe est: {code}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list, fail_silently = False)
            if send_mail:
                print("Email envoyé avec succès !")
                user.code_de_confirmation = code
                user.save()
                id = user.id
                return redirect("afficher_page_reinit_mot_de_passe", id = id)
            
        except User.DoesNotExist:
            pass  # L'adresse email n'est pas trouvée, vous pouvez afficher un message d'erreur

    return render(request, 'showtimeplan/mot_de_passe_oublie.html')
    
def afficher_page_reinit_mot_de_passe(request, id):
    return render(request, 'showtimeplan/reinit_mot_de_passe.html', {'id': id})


def traiter_reinit_mot_de_passe(request, id):
    if request.method == 'POST':
        code = int(request.POST['code'])
        mot_de_passe = request.POST['mot_de_passe']
        try:
            user = User.objects.get(id=id)
            if int(user.code_de_confirmation) == code:
                # Mettre à jour le mot de passe de l'utilisateur
                user.password = make_password(mot_de_passe)
                user.save()
                prenom_user = user.prenom
                return redirect("bienvenue_recuperation", prenom=prenom_user)
            else:
                error_message = "Le code saisi est incorrect! Réessayez !"
                return render(request, 'showtimeplan/reinit_mot_de_passe.html', {'error_message': error_message, 'id': id, 'code': code, 'mot_de_passe': mot_de_passe})
        except User.DoesNotExist:
            error_message = ""
            return render(request, 'showtimeplan/reinit_mot_de_passe.html', {'error_message': error_message, 'id': id, 'code': code, 'mot_de_passe': mot_de_passe})
    else:
        return redirect("afficher_page_reinit_mot_de_passe", id=id)
    
def bienvenue_recuperation(request, prenom):
    return render(request, 'showtimeplan/bienvenue_recuperation.html', {'prenom' : prenom})
