from django.shortcuts import render, redirect
from EditTimeplan import models
from EditTimeplan.models import CoursProgrammer
from EditTimeplan.models import CoursProgrammerL1
from EditTimeplan.models import AdminUser

def dashboardAdmin(request):
    cours_programmes = CoursProgrammer.objects.all()

    context = {
        'CoursProgrammer': cours_programmes,
                  }
    return render(request,'EditTimeplan/AdminPage2.html',context)
    
#Pour la promotion L1 tronc commun avec deux groupes
def save_cours(request):
    admin_id = request.session.get('admin_id')
    if request.method == 'POST':
        date = request.POST.get('date')
        jour = request.POST.get('day')
        heure_debut = request.POST.get('start-time')
        heure_fin = request.POST.get('end-time')
        matiere = request.POST.get('matiere')
        salle = request.POST.get('salle')
        groupe = request.POST.get('groupe')
        teacher = request.POST.get('professeur')
        #Recuperons l'admin en ligne pour lui permettre de modifier uniquement l'emploi du temps de ça promotion

        adminUser = AdminUser.objects.get(id=admin_id)
        cours = CoursProgrammerL1(
            date=date,
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
        cours_programmes = CoursProgrammerL1.objects.all()

        context = {
        'CoursProgrammer': cours_programmes,
                  }
    return render(request, 'EditTimeplan/AdminPage2.html',context)  

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

        #Recuperons l'admin en ligne pour lui permettre de modifier uniquement l'emploi du temps de sa promotion

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


