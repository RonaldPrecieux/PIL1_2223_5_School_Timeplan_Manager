from django.shortcuts import render
from showtimeplan.models import User

def formreg(request):
    return render(request, 'showtimeplan/index.html')
def insertuser(request):
    vunom=request.POST['nom'];
    vuprenom = request.POST['prenom'];#LES element entre crochets sont les nom de input dans le template
    vuemail = request.POST ['Email'];
    vuborn = request.POST['borndate'];
    us=User(nom = vunom,prenom = vuprenom, Email = vuemail,date_de_naissance=vuborn);
    us.save()
    return render(request,'showtimeplan/index.html',{})