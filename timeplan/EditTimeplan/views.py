from django.shortcuts import render, redirect
from EditTimeplan import models
from EditTimeplan.models import CoursProgrammer
from EditTimeplan.models import CoursProgrammerL1
from EditTimeplan.models import AdminUser

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
    return render(request, 'EditTimeplan/AdminPage.html') 

#Pour les autre promotions
def save_coursAll(request):
    id= request.session.get('id')
    if request.method == 'POST':
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
            jour=jour,
            promotion=adminUser.promotion,
            heure_debut=heure_debut,
            heure_fin=heure_fin,
            matiere=matiere,
            salle=salle,
            teacher=teacher,
            
        )
        cours.save()
        

    return render(request, 'EditTimeplan/AdminPage.html') 
from django.shortcuts import get_object_or_404

def Modify(request):
    if request.method == "POST":
        id=request.POST.get('id_cours_modif')
        try:
            cours = get_object_or_404(CoursProgrammerL1, id=id)
            cours.jour = request.POST.get('day')
            cours.heure_debut = request.POST.get('start-time')
            cours.heure_fin = request.POST.get('end-time')
            cours.matiere = request.POST.get('matiere')
            cours.salle = request.POST.get('salle')
            cours.groupe = request.POST.get('groupe')
            cours.teacher = request.POST.get('professeur')
            cours.save()  # N'oubliez pas de sauvegarder les modifications dans la base de données

            cours_programmes = CoursProgrammerL1.objects.all()
            context = {
                'CoursProgrammer': cours_programmes,
            }
            return redirect('dashboardAdmin')
            
        except CoursProgrammerL1.DoesNotExist:
            erreur = 'Ce cours n\'existe pas'
            context = {
                'erreur': erreur,
            }
    else:
        context = {}  # Assurez-vous de définir un contexte vide si la méthode de requête est différente de "POST"
    
    return render(request, 'EditTimeplan/AdminPage.html', context)


