from django.shortcuts import render, redirect
from EditTimeplan import models
from EditTimeplan.models import CoursProgrammer
from EditTimeplan.models import CoursProgrammerL1
from EditTimeplan.models import AdminUser,Matiere
from showtimeplan.models import CoursProgrammerL1Etu
from showtimeplan.models import  User
from django.conf import settings
from django.core.mail import send_mail
from django.db import connection
from datetime import datetime, timedelta
from django.http import HttpResponse
#######################################################Fonctions des dates####################################
def dates_semaine(date):
    jour_semaine = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    #date_obj = datetime.strptime(date, '%d %B %Y')  # Convertir la date en objet datetime
    date_obj=date
    jours_de_la_date= date_obj.weekday()  # Numéro du jour de la semaine

    # Calculer la date du lundi de cette semaine
    lundi_semaine = date_obj - timedelta(days=jours_de_la_date)

    # Créer une liste des dates de la semaine
    dates = [lundi_semaine + timedelta(days=i) for i in range(7)]

    # Formater les dates en chaînes de caractères
    dates_formattees = [date.strftime('%d %B %Y') for date in dates]

    return dates_formattees



def obtenir_jour(date):
    jours_semaine = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    date_obj = datetime.strptime(date, '%d %B %Y')  # Convertir la date en objet datetime
    jour = jours_semaine[date_obj.weekday()]  # Récupérer le jour de la semaine
    return jour

    #date_reference = datetime.strptime(une_date_de_la_semaine, '%d %B %Y')  # Convertir la date en objet datetime



def obtenir_date(jour_recherche, date_reference):
    jours_semaine = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

    # Trouver l'indice du jour recherché dans la liste jours_semaine
    indice_jour_recherche = jours_semaine.index(jour_recherche.capitalize())

    # Calculer la différence de jours entre le jour recherché et le jour de la date de référence
    difference_jours = indice_jour_recherche - date_reference.weekday()

    # Ajouter ou soustraire les jours nécessaires pour obtenir la date correspondante
    if difference_jours >= 0:
        date_obtenue = date_reference + timedelta(days=difference_jours)
    else:
        date_obtenue = date_reference - timedelta(days=abs(difference_jours))

    return date_obtenue.strftime('%d %B %Y')



def obtenir_la_date_du_Lundi(indexSem):#Prend le nombre de semaine a ajouter a la semaine actuelle et retourne une date dans la semaine demander
    date_aujourdhui=datetime.today().date()
    fin_semaine=datetime.strptime(obtenir_date('Dimanche',date_aujourdhui),'%d %B %Y')
    date_Lundi= fin_semaine + timedelta(days=indexSem*7)
    return date_Lundi.strftime('%d %B %Y')


###########################Afficharge du dashboard en fonction de la seamine la semaine par defaut est la semaine actuelle########################

def dashboardAdmin(request,label=0):#0=Cette semaine,1=Semaine prochaine
    if request.method == "POST":
        label = int(request.POST.get('week'))
      
    if label == 0:
        date_aujourdhui = datetime.today().date()  # Date de référence 
        les_dates_semaine = dates_semaine(date_aujourdhui)
        request.session['date_reference'] = date_aujourdhui.strftime('%d %B %Y')
        request.session['label'] = label
        id = request.session.get('id')  # Il transporte l'id de l'admin de la page de connexion vers la fonction de sauvegarde
        request.session['id'] = id
        cours_programmes = CoursProgrammerL1.objects.filter(Date__in=les_dates_semaine).order_by('heure_debut')
        matiere_obj = Matiere.objects.all()
        InfoSchedule = 'Vous modifiez l\'emploi du temps de cette semaine'
        context = {
            'InfoSchedule': InfoSchedule,
            'CoursProgrammer': cours_programmes,
            'matieres': matiere_obj,
        }
        return render(request, 'EditTimeplan/AdminPage.html', context)
    
    if label == 1:
        Une_date_de_la_semaine = datetime.strptime(obtenir_la_date_du_Lundi(1), '%d %B %Y')
        print(Une_date_de_la_semaine)
        request.session['date_reference'] = Une_date_de_la_semaine.strftime('%d %B %Y')
        request.session['label'] = label
        print(Une_date_de_la_semaine)
        les_dates_semaine = dates_semaine(Une_date_de_la_semaine)

        id = request.session.get('id')  # Il transporte l'id de l'admin de la page de connexion vers la fonction de sauvegarde
        request.session['id'] = id
        cours_programmes = CoursProgrammerL1.objects.filter(Date__in=les_dates_semaine).order_by('heure_debut')
        matiere_obj = Matiere.objects.all()
        InfoSchedule = 'Vous modifiez l\'emploi du temps de la semaine prochaine'
        context = {
            'InfoSchedule': InfoSchedule,
            'CoursProgrammer': cours_programmes,
            'matieres': matiere_obj,
        }
        return render(request, 'EditTimeplan/AdminPage.html', context)
    
    if label == 2:
        custom_date = request.POST.get('custom_date')
        if custom_date:
            custom_date = datetime.strptime(custom_date, '%Y-%m-%d').date()
        else:
        # Si custom_date est None, utilisez une valeur par défaut ou renvoyez une réponse d'erreur appropriée
            return HttpResponse("Invalid custom_date value.")
    
        les_dates_semaine = dates_semaine(custom_date)
        request.session['date_reference'] = custom_date.strftime('%Y-%m-%d')
        request.session['label'] = label
        id = request.session.get('id')
        request.session['id'] = id
        cours_programmes = CoursProgrammerL1.objects.filter(Date__in=les_dates_semaine).order_by('heure_debut')
        matiere_obj = Matiere.objects.all()
        InfoSchedule = 'Vous modifiez l\'emploi du temps de la semaine du ' + custom_date.strftime('%Y-%m-%d')
        context = {
            'InfoSchedule': InfoSchedule,
            'CoursProgrammer': cours_programmes,
            'matieres': matiere_obj,
        }
        return render(request, 'EditTimeplan/AdminPage.html', context)

    return HttpResponse("Invalid label value.")
def save_cours(request):
    id = request.session.get('id')
    date_reference = request.session.get('date_reference')
    label = request.session.get('label')
    if request.method == 'POST':
        jour = request.POST.get('day')
        date_reference = datetime.strptime(date_reference, '%d %B %Y')
        Date = obtenir_date(jour, date_reference)
        heure_debut = request.POST.get('start-time')
        heure_fin = request.POST.get('end-time')
        matiere = request.POST.get('matiere')
        salle = request.POST.get('salle')
        groupe = request.POST.get('groupe')
        teacher = request.POST.get('professeur')
        
        adminUser = AdminUser.objects.get(id=id)
        matiere_obj = Matiere.objects.get(nom=matiere)

        cours = CoursProgrammerL1(
            Date=Date,
            jour=jour.capitalize(),
            promotion=adminUser.promotion,
            heure_debut=heure_debut,
            heure_fin=heure_fin,
            matiere=matiere_obj,
            salle=salle,
            teacher=matiere_obj.enseignant,
            groupe=groupe
        )
        cours.save()

        return redirect('dashboardAdmin', label=label)
    
    return redirect('dashboardAdmin', id=1)
#Pour les autre promotions
def save_coursAll(request):
    id= request.session.get('id')
    if request.method == 'POST':
        date = request.POST.get('date')
        jour = request.POST.get('day')
        #promotion = request.POST.get('promotion')
        heure_debut = request.POST.get('start-time')
        heure_fin = request.POST.get('end-time')
        matiere = request.POST.get('matiere')
        salle = request.POST.get('salle')
        #teacher = request.POST.get('professeur') 
        #Recuperons l'admin en ligne pour lui permettre de modifier uniquement l'emplois du temps de ca promotion
        adminUser= AdminUser.objects.get(id=id)
        matiere_obj=Matiere.objects.get(nom=matiere)
        cours = CoursProgrammer(
            Date = date,
            jour=jour,
            promotion=adminUser.promotion,
            heure_debut=heure_debut,
            heure_fin=heure_fin,
            matiere=matiere_obj,
            salle=salle,
            teacher=matiere_obj.enseignant,
            
        )
        cours.save()
        

    redirect('dashboardAdmin')

from django.shortcuts import get_object_or_404
#Les fonction Modify et Delete sont specifique a la table CoursProgrammerL1 

def Modify(request):
    if request.method == "POST":
        id=request.POST.get('id_cours_modif')
        label=request.session.get('label')
        try:
            cours = get_object_or_404(CoursProgrammerL1, id=id)
          
            cours.jour = request.POST.get('day')
            cours.heure_debut = request.POST.get('start-time')
            cours.heure_fin = request.POST.get('end-time')
            nomMat=request.POST.get('matiere')
            matiere_obj=Matiere.objects.get(nom=nomMat)
            cours.matiere =matiere_obj
            cours.salle = request.POST.get('salle')
            cours.groupe = request.POST.get('groupe')
            cours.teacher = cours.matiere.enseignant
            cours.save()  

            return redirect('dashboardAdmin',label=label)
            
        except CoursProgrammerL1.DoesNotExist:
            erreur = 'Ce cours n\'existe pas'
            context = {
                'erreur': erreur,
            }
    else:
      return redirect('dashboardAdmin',label=label)

def DeleteCours(request,id):
    label=request.session.get('label')
    print(id)
    cours = get_object_or_404(CoursProgrammerL1, id=id)
    cours.delete()
    return redirect('dashboardAdmin',label=label)
##########################################################################

def copier_table(request):
    if request.method == 'POST':
        label_str = request.POST.get('week')
        label = int(label_str) if label_str is not None else 0
        with connection.cursor() as cursor:
            # Supprimer les données de la table de destination
            cursor.execute('DELETE FROM coursProgrammerL1Etu')

            # Copier les données de la table source vers la table de destination
            cursor.execute('INSERT INTO coursProgrammerL1Etu (Date, jour, promotion, heure_debut, heure_fin, matiere_id, salle, teacher, groupe) SELECT Date, jour, promotion, heure_debut, heure_fin, matiere_id, salle, teacher, groupe FROM coursProgrammerL1')
           #Envoyer un mail pour informer les étudiants que l'emploi du temps a été modifié
        etudiants = User.objects.values_list('email', flat=True)
        subject = 'Modification de l\'emploi du temps'
        message = 'Nous vous informons, chers étudiants, que l\'emploi du temps a été modifié.\nConnectez vous à la pateforme de SchedEase pour en savoir davantage.\n\nCordialement.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = list(etudiants)
        send_mail(subject, message, email_from, recipient_list, fail_silently=False)

    return redirect('dashboardAdmin',label=label)



