from django.shortcuts import render, redirect
from showtimeplan.forms import UserForm
from showtimeplan.models import User,CoursProgrammerL1Etu,CoursProgrammerEtu
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import views as auth_views
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from EditTimeplan.models import AdminUser,Matiere,Filiere
import random
from datetime import datetime, timedelta
from django.http import HttpResponse

from EditTimeplan.views import dates_semaine,obtenir_jour,obtenir_date,obtenir_la_date_du_Lundi


    
def access_denied(request):
    error_message = "Vous n'êtes pas autorisé à accéder à cette page sans vous connecter."
    return render(request, 'showtimeplan/access_denied.html', {'error_message': error_message})

   
 #Vue de création de compte avec mot de passe haché
#############################################################################

def insertuser(request):

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'Email déjà utilisé')
            else:
                user = form.save(commit=False)
                password = form.cleaned_data['mot_de_passe'] #Ca sert à récupérer un mot de passe propre pour faciliter le hachage 
                hashed_password = make_password(password)
                user.mot_de_passe = hashed_password
                user.save()
                prenom_user = form.cleaned_data['prenom']
                return redirect("dashboardStudent")
    else:
        form = UserForm()

    context = {'form': form}
    return render(request, 'showtimeplan/register.html', context)

################################################################################
def index(request):
    return render(request, "showtimeplan/index.html")

#################################################################################
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        mot_de_passe = request.POST.get('mot_de_passe')

        # Recherche de l'utilisateur dans la première table (AdminUser)
        try:
            admin_user = AdminUser.objects.get(email=email)
            if check_password(mot_de_passe, admin_user.mot_de_passe):
                request.session['id'] = admin_user.id
                return redirect('dashboardAdmin',label=0)
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
                return redirect('dashboardStudent')
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

######################################################################################################


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
###########################################Code Niveau Affichage Dashboard ####################################################
def dashboardStudent(request,label=0, filtre=False,Promotion='L1'):
    
    if request.method == "POST":
       Promotion_str=request.POST.get('filtre-Promotion')
       label_str = request.POST.get('week')
       label = int(label_str) if label_str is not None else 0
       Promotion=str(Promotion_str) if Promotion_str is not None else "L1"
       #filiereid=Filiere.objects.get(nom='Licence 1')
       filtre=request.POST.get('filtre')
       custom_date=request.POST.get('custom_date')

       nomprof=request.POST.get('nomprof')
       if filtre=='3':
           filtre=False
    print(Promotion)
    if filtre :
        if label==0:
            date_aujourdhui = datetime.today().date() # Date de référence 
            les_dates_semaine = dates_semaine(date_aujourdhui)
            request.session['date_reference']=date_aujourdhui.strftime('%d %B %Y')
            request.session['label']=label
            id= request.session.get('id')#Il transporte l'id de l'admin de la page de coneexion vers la fonction de sauvegarde
            request.session['id']=id
            if Promotion == 'L1':
                cours_programmes = CoursProgrammerL1Etu.objects.filter(Date__in= les_dates_semaine).order_by('heure_debut')  # Ajout de order_by()
                if filtre=='Groupe1' or filtre=='Groupe2':
                    cours_programmes = CoursProgrammerL1Etu.objects.filter(Date__in= les_dates_semaine,groupe__in=[filtre,'Groupe 1 & Groupe 2'],promotion=Promotion).order_by('heure_debut')  # Ajout de order_by()
            
                if filtre=='enseignant':
                    cours_programmes = CoursProgrammerL1Etu.objects.filter(Date__in= les_dates_semaine,teacher=nomprof,promotion=Promotion).order_by('heure_debut') 
                # Le double souligné __in indique que nous voulons filtrer les cours avec une date présente dans la liste.
            else:
                cours_programmes = CoursProgrammerEtu.objects.filter(Date__in= les_dates_semaine).order_by('heure_debut')  # Ajout de order_by()
                if filtre=='Groupe1' or filtre=='Groupe2':
                    cours_programmes = CoursProgrammerEtu.objects.filter(Date__in= les_dates_semaine,groupe__in=[filtre,'Groupe 1 & Groupe 2'],promotion=Promotion).order_by('heure_debut')  # Ajout de order_by()
            
                if filtre=='enseignant':
                    cours_programmes = CoursProgrammerEtu.objects.filter(Date__in= les_dates_semaine,teacher=nomprof,promotion=Promotion).order_by('heure_debut') 
                
            matiere_obj=Matiere.objects.all()
            InfoSchedule='de la '+Promotion+'cette semaine'
           
            NomFiltre='Filtre='+filtre


            context = {
                'filtre':NomFiltre,
                'InfoSchedule': InfoSchedule,
                'CoursProgrammer': cours_programmes,
                'matieres':matiere_obj,
                            }
            return render(request,'showtimeplan/dashboardEtu.html',context)
        if label==1:
            Une_date_de_la_semaine=datetime.strptime(obtenir_la_date_du_Lundi(1),'%d %B %Y')
            print(Une_date_de_la_semaine)
            request.session['date_reference']=Une_date_de_la_semaine.strftime('%d %B %Y')
            request.session['label']=label
            print(Une_date_de_la_semaine)
            les_dates_semaine = dates_semaine(Une_date_de_la_semaine)

            id= request.session.get('id')#Il transporte l'id de l'admin de la page de coneexion vers la fonction de sauvegarde
            request.session['id']=id
            if Promotion == 'L1':
                cours_programmes = CoursProgrammerL1Etu.objects.filter(Date__in= les_dates_semaine).order_by('heure_debut')  # Ajout de order_by()
                if filtre=='Groupe1' or filtre=='Groupe2':
                    cours_programmes = CoursProgrammerL1Etu.objects.filter(Date__in= les_dates_semaine,groupe__in=[filtre,'Groupe 1 & Groupe 2'],promotion=Promotion).order_by('heure_debut')  # Ajout de order_by()
            
                if filtre=='enseignant':
                    cours_programmes = CoursProgrammerL1Etu.objects.filter(Date__in= les_dates_semaine,teacher=nomprof,promotion=Promotion).order_by('heure_debut') 
                # Le double souligné __in indique que nous voulons filtrer les cours avec une date présente dans la liste.
            else:
                cours_programmes = CoursProgrammerEtu.objects.filter(Date__in= les_dates_semaine).order_by('heure_debut')  # Ajout de order_by()
                if filtre=='Groupe1' or filtre=='Groupe2':
                    cours_programmes = CoursProgrammerEtu.objects.filter(Date__in= les_dates_semaine,groupe__in=[filtre,'Groupe 1 & Groupe 2'],promotion=Promotion).order_by('heure_debut')  # Ajout de order_by()
            
                if filtre=='enseignant':
                    cours_programmes = CoursProgrammerEtu.objects.filter(Date__in= les_dates_semaine,teacher=nomprof,promotion=Promotion).order_by('heure_debut') 
            matiere_obj=Matiere.objects.all()
            InfoSchedule='de la '+Promotion+' de la semaine prochaine'
           
            NomFiltre='Filtre='+filtre


            context = {
                'filtre':NomFiltre,
                'InfoSchedule': InfoSchedule,
                'CoursProgrammer': cours_programmes,
                'matieres':matiere_obj,
                            }
            return render(request,'showtimeplan/dashboardEtu.html',context)
        
        #Semaine passé 
        if label==3:
            Une_date_de_la_semaine=datetime.strptime(obtenir_la_date_du_Lundi(-1),'%d %B %Y')
            print(Une_date_de_la_semaine)
            request.session['date_reference']=Une_date_de_la_semaine.strftime('%d %B %Y')
            request.session['label']=label
            print(Une_date_de_la_semaine)
            les_dates_semaine = dates_semaine(Une_date_de_la_semaine)

            id= request.session.get('id')#Il transporte l'id de l'admin de la page de coneexion vers la fonction de sauvegarde
            request.session['id']=id
            if Promotion == 'L1':
                cours_programmes = CoursProgrammerL1Etu.objects.filter(Date__in= les_dates_semaine).order_by('heure_debut')  # Ajout de order_by()
                if filtre=='Groupe1' or filtre=='Groupe2':
                    cours_programmes = CoursProgrammerL1Etu.objects.filter(Date__in= les_dates_semaine,groupe__in=[filtre,'Groupe 1 & Groupe 2'],promotion=Promotion).order_by('heure_debut')  # Ajout de order_by()
            
                if filtre=='enseignant':
                    cours_programmes = CoursProgrammerL1Etu.objects.filter(Date__in= les_dates_semaine,teacher=nomprof,promotion=Promotion).order_by('heure_debut') 
                # Le double souligné __in indique que nous voulons filtrer les cours avec une date présente dans la liste.
            else:
                cours_programmes = CoursProgrammerEtu.objects.filter(Date__in= les_dates_semaine).order_by('heure_debut')  # Ajout de order_by()
                if filtre=='Groupe1' or filtre=='Groupe2':
                    cours_programmes = CoursProgrammerEtu.objects.filter(Date__in= les_dates_semaine,groupe__in=[filtre,'Groupe 1 & Groupe 2'],promotion=Promotion).order_by('heure_debut')  # Ajout de order_by()
            
                if filtre=='enseignant':
                    cours_programmes = CoursProgrammerEtu.objects.filter(Date__in= les_dates_semaine,teacher=nomprof,promotion=Promotion).order_by('heure_debut') 
            matiere_obj=Matiere.objects.all()
            InfoSchedule='de la '+Promotion+'la semaine passé'
           
            NomFiltre='Filtre='+filtre


            context = {
                'filtre':NomFiltre,
                'InfoSchedule': InfoSchedule,
                'CoursProgrammer': cours_programmes,
                'matieres':matiere_obj,
                            }
            return render(request,'showtimeplan/dashboardEtu.html',context)
        
        
        if label==2:
            custom_date=request.POST.get('custom_date')
            custom_date=datetime.strptime(custom_date,'%Y-%B-%d')#######Il y a un gros probleme de format ici######
            print(custom_date)
            les_dates_semaine=dates_semaine(custom_date)
            request.session['date_reference']=(custom_date).strftime('%Y-%m-%d')
            request.session['label']=label
            id= request.session.get('id')#Il transporte l'id de l'admin de la page de coneexion vers la fonction de sauvegarde
            request.session['id']=id
            if Promotion == 'L1':
                cours_programmes = CoursProgrammerL1Etu.objects.filter(Date__in= les_dates_semaine).order_by('heure_debut')  # Ajout de order_by()
                if filtre=='Groupe1' or filtre=='Groupe2':
                    cours_programmes = CoursProgrammerL1Etu.objects.filter(Date__in= les_dates_semaine,groupe__in=[filtre,'Groupe 1 & Groupe 2'],promotion=Promotion).order_by('heure_debut')  # Ajout de order_by()
            
                if filtre=='enseignant':
                    cours_programmes = CoursProgrammerL1Etu.objects.filter(Date__in= les_dates_semaine,teacher=nomprof,promotion=Promotion).order_by('heure_debut') 
                # Le double souligné __in indique que nous voulons filtrer les cours avec une date présente dans la liste.
            else:
                cours_programmes = CoursProgrammerEtu.objects.filter(Date__in= les_dates_semaine).order_by('heure_debut')  # Ajout de order_by()
                if filtre=='Groupe1' or filtre=='Groupe2':
                    cours_programmes = CoursProgrammerEtu.objects.filter(Date__in= les_dates_semaine,groupe__in=[filtre,'Groupe 1 & Groupe 2'],promotion=Promotion).order_by('heure_debut')  # Ajout de order_by()
            
                if filtre=='enseignant':
                    cours_programmes = CoursProgrammerEtu.objects.filter(Date__in= les_dates_semaine,teacher=nomprof,promotion=Promotion).order_by('heure_debut') 
            # Le double souligné __in indique que nous voulons filtrer les cours avec une date présente dans la liste.
            matiere_obj=Matiere.objects.all()
            InfoSchedule='de la '+Promotion+' de la semaine du'+custom_date
           
            NomFiltre='Filtre='+filtre


            context = {
                'filtre':NomFiltre,
                'InfoSchedule': InfoSchedule,
                'CoursProgrammer': cours_programmes,
                'matieres':matiere_obj,
                            }
            return render(request,'showtimeplan/dashboardEtu.html',context)
        # Si aucun des cas précédents n'est satisfait, renvoyer une réponse HTTP par défaut
        return HttpResponse("Invalid label value.")
    #Else du filtre
    else: 
        if label==0:
            date_aujourdhui = datetime.today().date() # Date de référence 
            les_dates_semaine = dates_semaine(date_aujourdhui)
            request.session['date_reference']=date_aujourdhui.strftime('%d %B %Y')
            request.session['label']=label
            id= request.session.get('id')#Il transporte l'id de l'admin de la page de coneexion vers la fonction de sauvegarde
            request.session['id']=id
            if Promotion == 'L1':
                cours_programmes = CoursProgrammerL1Etu.objects.filter(Date__in= les_dates_semaine).order_by('heure_debut') 
            # Le double souligné __in indique que nous voulons filtrer les cours avec une date présente dans la liste.
            else:
                  cours_programmes = CoursProgrammerEtu.objects.filter(Date__in= les_dates_semaine,promotion=Promotion).order_by('heure_debut') 
            matiere_obj=Matiere.objects.all()
            InfoSchedule=' la '+Promotion+' cette semaine'

            context = {
                'InfoSchedule': InfoSchedule,
                'CoursProgrammer': cours_programmes,
                'matieres':matiere_obj,
                            }
            return render(request,'showtimeplan/dashboardEtu.html',context)
        if label==1:
            Une_date_de_la_semaine=datetime.strptime(obtenir_la_date_du_Lundi(1),'%d %B %Y')
            print(Une_date_de_la_semaine)
            request.session['date_reference']=Une_date_de_la_semaine.strftime('%d %B %Y')
            request.session['label']=label
            print(Une_date_de_la_semaine)
            les_dates_semaine = dates_semaine(Une_date_de_la_semaine)

            id= request.session.get('id')#Il transporte l'id de l'admin de la page de coneexion vers la fonction de sauvegarde
            request.session['id']=id
            if Promotion == 'L1':
                cours_programmes = CoursProgrammerL1Etu.objects.filter(Date__in= les_dates_semaine).order_by('heure_debut') 
            # Le double souligné __in indique que nous voulons filtrer les cours avec une date présente dans la liste.
            else:
                 cours_programmes = CoursProgrammerEtu.objects.filter(Date__in= les_dates_semaine,promotion=Promotion).order_by('heure_debut')
            matiere_obj=Matiere.objects.all()
            InfoSchedule=' la '+Promotion+' de la semaine prochaine'
            context = {
                'InfoSchedule': InfoSchedule,
                'CoursProgrammer': cours_programmes,
                'matieres':matiere_obj,
                            }
            return render(request,'showtimeplan/dashboardEtu.html',context)
        #Semaine precedente
        if label==3:
            Une_date_de_la_semaine=datetime.strptime(obtenir_la_date_du_Lundi(-1),'%d %B %Y')
            print(Une_date_de_la_semaine)
            request.session['date_reference']=Une_date_de_la_semaine.strftime('%d %B %Y')
            request.session['label']=label
            print(Une_date_de_la_semaine)
            les_dates_semaine = dates_semaine(Une_date_de_la_semaine)

            id= request.session.get('id')#Il transporte l'id de l'admin de la page de coneexion vers la fonction de sauvegarde
            request.session['id']=id
            if Promotion == 'L1':
                cours_programmes = CoursProgrammerL1Etu.objects.filter(Date__in= les_dates_semaine).order_by('heure_debut')
            else :
                cours_programmes = CoursProgrammerEtu.objects.filter(Date__in= les_dates_semaine,promotion=Promotion).order_by('heure_debut')
            # Le double souligné __in indique que nous voulons filtrer les cours avec une date présente dans la liste.
            matiere_obj=Matiere.objects.all()
            InfoSchedule=' la '+Promotion+' la semaine passé'
            context = {
                'InfoSchedule': InfoSchedule,
                'CoursProgrammer': cours_programmes,
                'matieres':matiere_obj,
                            }
            return render(request,'showtimeplan/dashboardEtu.html',context)
        
        if label==2:
            custom_date=request.POST.get('custom_date')
            custom_date=datetime.strptime(custom_date,'%Y-%m-%d')#######Il y a un gros probleme de format ici######
            print(custom_date)
            les_dates_semaine=dates_semaine(custom_date)
            request.session['date_reference']=(custom_date).strftime('%Y-%B-%d')
            request.session['label']=label
            id= request.session.get('id')#Il transporte l'id de l'admin de la page de coneexion vers la fonction de sauvegarde
            request.session['id']=id
            if Promotion == 'L1':
                cours_programmes = CoursProgrammerL1Etu.objects.filter(Date__in= les_dates_semaine).order_by('heure_debut') 
            else:
                cours_programmes = CoursProgrammerEtu.objects.filter(Date__in= les_dates_semaine,promotion=Promotion).order_by('heure_debut')
            # Le double souligné __in indique que nous voulons filtrer les cours avec une date présente dans la liste.
            matiere_obj=Matiere.objects.all()
            InfoSchedule='de la'+Promotion+' de la semaine du '+custom_date.strftime('%d-%B-%Y')
            #InfoSchedule=' la '+filiere+'de la semaine du '+custom_date
            context = {
                'InfoSchedule': InfoSchedule,
                'CoursProgrammer': cours_programmes,
                'matieres':matiere_obj,
                            }
            return render(request,'showtimeplan/dashboardEtu.html',context)
        # Si aucun des cas précédents n'est satisfait, renvoyer une réponse HTTP par défaut
        return HttpResponse("Invalid label value.")


def PlusInfo(request,id):
    matiere_Ins=Matiere.objects.get(id=id) #Instance de la matiere
    context={
        'matiere':matiere_Ins,
    }
    print(id)
    return render(request,'showtimeplan/plusinfo.html',context)

