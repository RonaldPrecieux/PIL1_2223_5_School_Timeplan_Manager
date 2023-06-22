from django.shortcuts import render, redirect
from showtimeplan.forms import UserForm
from showtimeplan.models import User
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import views as auth_views
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from EditTimeplan.models import AdminUser
import random

def insertuser(request): #Vue de création de compte avec mot de passe haché
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'Email déjà utilisé')
            else:
                user = form.save(commit=False)
                password = form.cleaned_data['mot_de_passe']
                hashed_password = make_password(password)
                user.mot_de_passe = hashed_password
                user.save()
                prenom_user = form.cleaned_data['prenom']
                return redirect("bienvenue", prenom=prenom_user)
    else:
        form = UserForm()

    context = {'form': form}
    return render(request, 'showtimeplan/register.html', context)


def index(request):
    return render(request, "showtimeplan/index.html")


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        mot_de_passe = request.POST.get('mot_de_passe')

        # Recherche de l'utilisateur dans la première table (AdminUser)
        try:
            admin_user = AdminUser.objects.get(email=email)
            if check_password(mot_de_passe, admin_user.mot_de_passe):
                return redirect('bienvenue_connexion', prenom=admin_user.prenom)
            else:
                context = {
                    'error_message': 'Email ou mot de passe incorrect. Réessayez !',
                    'email_value': email,  
                    'password_value': mot_de_passe,
                }
                return render(request, 'showtimeplan/login.html', context)
        except AdminUser.DoesNotExist:
            pass

        # Recherche de l'utilisateur dans la seconde table (User)
        try:
            user = User.objects.get(email=email)
            if check_password(mot_de_passe, user.mot_de_passe):
                return redirect('bienvenue_connexion', prenom=user.prenom)
            else:
                context = {
                    'error_message': 'Email ou mot de passe incorrect. Réessayez !',
                    'email_value': email,  
                    'password_value': mot_de_passe,
                }
                return render(request, 'showtimeplan/login.html', context)
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
            admin_user = AdminUser.objects.get(email=email)
            code = random.randint(100000, 999999)
            admin_user.reset_code = code
            admin_user.save()
            
            # Envoyer l'email de réinitialisation pour l'administrateur
            subject = 'Réinitialisation du mot de passe (Admin)'
            message = f'Votre code de réinitialisation du mot de passe est : {code}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list, fail_silently=False)
            if send_mail:
                print("Email envoyé avec succès (Admin) !")
                admin_user.Code_confirmation = code
                admin_user.save()
                id = admin_user.id
                return redirect("afficher_page_reinit_mot_de_passe", id=id)
        
        except AdminUser.DoesNotExist:
            try:
                user = User.objects.get(email=email)
                code = random.randint(100000, 999999)
                user.reset_code = code
                user.save()
                
                # Envoyer l'email de réinitialisation pour l'utilisateur
                subject = 'Réinitialisation du mot de passe (User)'
                message = f'Votre code de réinitialisation du mot de passe est : {code}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]
                send_mail(subject, message, email_from, recipient_list, fail_silently=False)
                if send_mail:
                    print("Email envoyé avec succès (User) !")
                    user.code_de_confirmation = code
                    user.save()
                    id = user.id
                    return redirect("afficher_page_reinit_mot_de_passe", id=id)
            
            except User.DoesNotExist:
                pass  # L'adresse email n'est pas trouvée dans aucune des tables, vous pouvez afficher un message d'erreur

    return render(request, 'showtimeplan/mot_de_passe_oublie.html')
    
def afficher_page_reinit_mot_de_passe(request, id):
    return render(request, 'showtimeplan/reinit_mot_de_passe.html', {'id': id})


def traiter_reinit_mot_de_passe(request, id):
    if request.method == 'POST':
        code = int(request.POST['code'])
        mot_de_passe = request.POST['mot_de_passe']
        
        try:
            admin_user = AdminUser.objects.get(id=id)
            if int(admin_user.Code_confirmation) == code:
                # Hacher le mot de passe
                mot_de_passe_hache = make_password(mot_de_passe)
                
                # Mettre à jour le mot de passe de l'administrateur
                admin_user.mot_de_passe = mot_de_passe_hache
                admin_user.save()
                
                prenom_admin = admin_user.prenom
                return redirect("bienvenue_recuperation", prenom=prenom_admin)
        except AdminUser.DoesNotExist:
            pass  # L'administrateur n'est pas trouvé dans la table AdminUser
        
        try:
            user = User.objects.get(id=id)
            if int(user.code_de_confirmation) == code:
                # Hacher le mot de passe
                mot_de_passe_hache = make_password(mot_de_passe)
                
                # Mettre à jour le mot de passe de l'utilisateur
                user.mot_de_passe = mot_de_passe_hache
                user.save()
                
                prenom_user = user.prenom
                return redirect("bienvenue_recuperation", prenom=prenom_user)
        except User.DoesNotExist:
            pass  # L'utilisateur n'est pas trouvé dans la table User
        
        # Le code ou l'utilisateur n'est pas trouvé dans aucune des tables
        error_message = "Le code saisi est incorrect ou l'utilisateur n'existe pas ! Réessayez !"
        return render(request, 'showtimeplan/reinit_mot_de_passe.html', {'error_message': error_message, 'id': id, 'code': code, 'mot_de_passe': mot_de_passe})
    
    else:
        return redirect("afficher_page_reinit_mot_de_passe", id=id)
    
def bienvenue_recuperation(request, prenom):
    return render(request, 'showtimeplan/bienvenue_recuperation.html', {'prenom' : prenom})

def login_required(request):
    return render(request, "showtimeplan/login_required.html")