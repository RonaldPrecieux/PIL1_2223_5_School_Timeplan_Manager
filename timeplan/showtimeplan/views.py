from django.shortcuts import render
from showtimeplan.models import User

def formreg(request):
    return render(request, 'showtimeplan/index.html')
def insertuser(request):
    vunom=request.POST['nom']
    vuprenom = request.POST['prenom'] #Les élements entre crochets sont les noms des input dans le template
    vuemail = request.POST ['Email']
    vuborn = request.POST['borndate']
    us=User(nom = vunom,prenom = vuprenom, Email = vuemail,date_de_naissance=vuborn)
    us.save()
    return render(request,'showtimeplan/index.html',{})

def index(request):
    return render(request, "showtimeplan/index_commite.html")

def login(request):
    return render(request, "showtimeplan/login.html")

def register(request):
    return render(request, "showtimeplan/register.html")

