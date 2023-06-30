from django.shortcuts import render, redirect
from EditTimeplan import models
from EditTimeplan.models import CoursProgrammer
from EditTimeplan.models import CoursProgrammerL1
from EditTimeplan.models import AdminUser,Matiere
from showtimeplan.models import CoursProgrammerL1Etu
from django.db import connection
from datetime import datetime, timedelta

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


def obtenir_date(jour, une_date_de_la_semaine):
    jours_semaine = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    date_reference =une_date_de_la_semaine

    # Trouver l'indice du jour de la semaine dans la liste jours_semaine
    indice_jour = jours_semaine.index(jour.capitalize())

    # Calculer la date correspondante en ajoutant ou en soustrayant des jours à la date de référence
    if indice_jour < date_reference.weekday():
        # Si l'indice du jour est inférieur au jour de la semaine de la date de référence,
        # nous devons revenir à la semaine précédente
        delta = timedelta(days=7 - (date_reference.weekday() - indice_jour))
    else:
        # Sinon, nous pouvons simplement soustraire les jours
        delta = timedelta(days=indice_jour - date_reference.weekday())

    date_obtenue = date_reference + delta

    return date_obtenue.strftime('%d %B %Y')


def obtenir_la_date_du_Lundi(indexSem):#Prend le nombre de semaine a ajouter a la semaine actuelle et retourne une date dans la semaine demander
    date_aujourdhui=datetime.today().date()
    fin_semaine=obtenir_date('Dimanche',date_aujourdhui)
    date_Lundi= fin_semaine + timedelta(days=indexSem*7)
    return date_Lundi

def dashboardAdmin(request):
    date_aujourdhui = datetime.today().date() # Date de référence 
    les_dates_semaine = dates_semaine(date_aujourdhui)

    id= request.session.get('id')#Il transporte l'id de l'admin de la page de coneexion vers la fonction de sauvegarde
    request.session['id']=id
    cours_programmes = CoursProgrammerL1.objects.filter(Date__in= les_dates_semaine)
    # Le double souligné __in indique que nous voulons filtrer les cours avec une date présente dans la liste.
    matiere_obj=Matiere.objects.all()
    context = {
        'CoursProgrammer': cours_programmes,
        'matieres':matiere_obj,
                  }
    return render(request,'EditTimeplan/AdminPage.html',context)
    
#Pour la promotion L1 tronc commun avec deux groupe
#PAR DEFAUT(Les cours de cette semaine)
def save_cours(request):
    id = request.session.get('id')
    if request.method == 'POST':
        jour = request.POST.get('day')
        date_reference = datetime.today().date()  # Date de référence (date actuelle)
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

        return redirect('dashboardAdmin')
    
    return redirect('dashboardAdmin')

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

            return redirect('dashboardAdmin')
            
        except CoursProgrammerL1.DoesNotExist:
            erreur = 'Ce cours n\'existe pas'
            context = {
                'erreur': erreur,
            }
    else:
       redirect('dashboardAdmin')

def DeleteCours(request,id):
    print(id)
    cours = get_object_or_404(CoursProgrammerL1, id=id)
    cours.delete()
    return redirect('dashboardAdmin')
##########################################################################

def copier_table(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            # Supprimer les données de la table de destination
            cursor.execute('DELETE FROM coursProgrammerL1Etu')

            # Copier les données de la table source vers la table de destination
            cursor.execute('INSERT INTO coursProgrammerL1Etu (Date, jour, promotion, heure_debut, heure_fin, matiere_id, salle, teacher, groupe) SELECT Date, jour, promotion, heure_debut, heure_fin, matiere_id, salle, teacher, groupe FROM coursProgrammerL1')

    return redirect('dashboardAdmin')



