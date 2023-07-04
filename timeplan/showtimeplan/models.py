from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.core.validators import MinLengthValidator
from EditTimeplan.models import Matiere,Filiere
from django.core.validators import RegexValidator

class User(models.Model):
    nom = models.CharField(max_length=120, validators=[MinLengthValidator(3)])
    prenom = models.CharField(max_length=120, validators=[MinLengthValidator(3)])
    email = models.EmailField(unique=True)
    numero_telephone = models.CharField(max_length=20)
    mot_de_passe = models.CharField(max_length=128)
    code_de_confirmation= models.IntegerField(null=True,default=None)
    
    class Meta:
        db_table = 'etudiants_enregistres'

def save(self, *args, **kwargs):
    # Hacher le mot de passe avant de l'enregistrer
    self.mot_de_passe = make_password(self.mot_de_passe)
    super(User, self).save(*args, **kwargs)
    

class CoursProgrammerL1Etu(models.Model):
    Date= models.CharField(default='10/05/2023', max_length=128 ,validators=[
            RegexValidator(
                regex=r'^\d{2}/\d{2}/\d{4}$',
                message='Le format de date doit être jj/mm/aaaa.',
            )
    ],)
    jour= models.CharField(max_length=128)
    promotion = models.CharField(max_length=128)
    heure_debut = models.CharField(max_length=150)
    heure_fin = models.CharField(max_length=150)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)  #A ce niveau fait attention Django a apellé la colone là matiere_id
    #matiere = models.CharField(max_length=150)
    salle = models.CharField(max_length=150)
    teacher=models.CharField(max_length=128, default='')
    groupe=models.CharField(max_length=128)  #Je veux que lorsque l'admin tape sur G1 ou G1 Groupe 1 ou..
    #Aparaisse dans la base de donné
    class Meta:
        db_table = "coursProgrammerL1Etu"



class CoursProgrammerEtu(models.Model):
    Date= models.CharField(default='10/05/2023', max_length=128 ,validators=[
            RegexValidator(
                regex=r'^\d{2}/\d{2}/\d{4}$',
                message='Le format de date doit être jj/mm/aaaa.',
            ),
        ],)
    jour = models.CharField(max_length=100)
    promotion = models.CharField(max_length=128)
    heure_debut = models.CharField(max_length=150)
    heure_fin = models.CharField(max_length=150)
    filiere=models.ForeignKey(Filiere, on_delete=models.CASCADE,default="")
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE,default="") 
    salle = models.CharField(max_length=150)
    teacher=models.CharField(max_length=128, default='')
    class Meta:
        db_table = "coursProgrammerEtu"


   
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


   
    
    