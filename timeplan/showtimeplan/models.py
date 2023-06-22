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
    

        