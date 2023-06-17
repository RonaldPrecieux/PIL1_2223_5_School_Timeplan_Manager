from django.db import models
from django.core.exceptions import ValidationError
class User(models.Model):
    nom = models.fields.CharField(max_length=100, default ="")
    prenom = models.fields.CharField(max_length=100, default ="")
    email = models.EmailField(unique=True, default="")
    numero_telephone = models.CharField(max_length=20, default= 555)
    mot_de_passe = models.CharField(max_length=128, default ="")
    confirmer_mot_de_passe = models.CharField(max_length=128, editable=False, default ="")
    
    def clean(self):
        # Vérifier si l'e-mail est déjà utilisé
        if User.objects.filter(email=self.email).exists():
            raise ValidationError("Cet e-mail est déjà utilisé.")


    """def save(self, *args, **kwargs):
        # Hacher le mot de passe avant de l'enregistrer
        self.mot_de_passe = make_password(self.mot_de_passe)
        super().save(*args, **kwargs)"""
    
    

    

        