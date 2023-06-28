from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.core.validators import MinLengthValidator

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
    
class CoursProgrammerEtu(models.Model):
    #date = models.DateField()
    jour = models.CharField(max_length=100)
    promotion = models.CharField(max_length=128)
    heure_debut = models.TimeField()  #Je reviendrais regler l'erreur de format qui se pose lorsqu'on met TimeField
    heure_fin = models.TimeField()
    matiere = models.CharField(max_length=150)
    salle = models.CharField(max_length=150)
    teacher=models.CharField(max_length=128, default='')
    class Meta:
        db_table = "coursProgrammerEtu"
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class CoursProgrammerL1Etu(models.Model):
    Date= models.DateField(default='2023-05-10')
    jour= models.CharField(max_length=128)
    promotion = models.CharField(max_length=128)
    heure_debut = models.CharField(max_length=150)
    heure_fin = models.CharField(max_length=150)
    matiere = models.CharField(max_length=150)
    salle = models.CharField(max_length=150)
    teacher=models.CharField(max_length=128, default='')
    groupe=models.CharField(max_length=128) #Ce modèle est exactement la copie de l'autre coursprogrammer dans EditTimeplan. Lorsque l'utilisateur clique sur le bouton publier les lignes de l'autre table sont copiés vers cette table.
    #Aparaisse dans la base de données
    class Meta:
        db_table = "coursProgrammerL1Etu"


   
    
    