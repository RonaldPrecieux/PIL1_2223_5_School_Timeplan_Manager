from django.shortcuts import render, redirect
from showtimeplan.forms import UserForm
from showtimeplan.models import User
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

def cherche_le_compte(request):
    if request.method == 'POST':
        email=request.POST['email']
        try:
            user=User.objects.get(email=email)
            context={
                'prenom':user.prenom,
                'nom':user.nom
            }
            return redirect('recuperation_compte',context )
        except User.DoesNotExist:
            context={
                'prenom':user.prenom,
                'nom':user.nom
            }
            return redirect('account_no_found',context)
