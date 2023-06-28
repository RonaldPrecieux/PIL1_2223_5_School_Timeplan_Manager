from django.shortcuts import render, redirect
from EditTimeplan import models
from EditTimeplan.models import CoursProgrammer
from EditTimeplan.models import CoursProgrammerL1
from EditTimeplan.models import AdminUser
from showtimeplan.models import CoursProgrammerL1Etu
from django.db import connection

def dashboardAdmin(request):
    id= request.session.get('id')
    request.session['id']=id
    cours_programmes = CoursProgrammerL1.objects.all()

    context = {
        'CoursProgrammer': cours_programmes,
                  }
    return render(request,'EditTimeplan/AdminPage.html',context)
    
#Pour la promotion L1 tronc commun avec deux groupe
def save_cours(request):
    id= request.session.get('id')
    if request.method == 'POST':
        date = request.POST.get('date')
        jour = request.POST.get('day')
        heure_debut = request.POST.get('start-time')
        heure_fin = request.POST.get('end-time')
        matiere = request.POST.get('matiere')
        salle = request.POST.get('salle')
        groupe = request.POST.get('groupe')
        teacher = request.POST.get('professeur')
        #Recuperons l'admin en ligne pour lui permettre de modifier uniquement l'emplois du temps de ca promotion
        adminUser= AdminUser.objects.get(id=id)
        print(id)
        cours = CoursProgrammerL1(
            Date = date,
            jour=jour,
            promotion=adminUser.promotion,
            heure_debut=heure_debut,
            heure_fin=heure_fin,
            matiere=matiere,
            salle=salle,
            teacher=teacher,
            groupe=groupe
            
        )
        cours.save()
        #cours_programmes = CoursProgrammerL1.objects.all()

       #context = {
        #'CoursProgrammer': cours_programmes,
         #         }
        return redirect('dashboardAdmin') 
    redirect('dashboardAdmin')

#Pour les autre promotions
def save_coursAll(request):
    id= request.session.get('id')
    if request.method == 'POST':
        date = request.POST.get('date')
        jour = request.POST.get('day')
        promotion = request.POST.get('promotion')
        heure_debut = request.POST.get('start-time')
        heure_fin = request.POST.get('end-time')
        matiere = request.POST.get('matiere')
        salle = request.POST.get('salle')
        teacher = request.POST.get('professeur')
        #Recuperons l'admin en ligne pour lui permettre de modifier uniquement l'emplois du temps de ca promotion
        adminUser= AdminUser.objects.get(id=id)
        
        cours = CoursProgrammer(
            Date = date,
            jour=jour,
            promotion=adminUser.promotion,
            heure_debut=heure_debut,
            heure_fin=heure_fin,
            matiere=matiere,
            salle=salle,
            teacher=teacher,
            
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
            cours.Date = request.POST.get('date')
            cours.jour = request.POST.get('day')
            cours.heure_debut = request.POST.get('start-time')
            cours.heure_fin = request.POST.get('end-time')
            cours.matiere = request.POST.get('matiere')
            cours.salle = request.POST.get('salle')
            cours.groupe = request.POST.get('groupe')
            cours.teacher = request.POST.get('professeur')
            cours.save()  # N'oubliez pas de sauvegarder les modifications dans la base de données

           # cours_programmes = CoursProgrammerL1.objects.all()
           # context = {
           #     'CoursProgrammer': cours_programmes,
            #}
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

def copier_table(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            # Supprimer les données de la table de destination
            cursor.execute('DELETE FROM coursProgrammerL1Etu')

            # Copier les données de la table source vers la table de destination
            cursor.execute('INSERT INTO coursProgrammerL1Etu (Date, jour, promotion, heure_debut, heure_fin, matiere, salle, teacher, groupe) SELECT Date, jour, promotion, heure_debut, heure_fin, matiere, salle, teacher, groupe FROM coursProgrammerL1')

    return redirect('dashboardAdmin')



