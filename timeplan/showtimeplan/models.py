from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
class User(models.Model):
    nom = models.fields.CharField(max_length=100)
    prenom = models.fields.CharField(max_length=100)
    date_de_naissance = models.fields.DateField()
    Email=models.fields.EmailField()
    class Meta:
        db_table="etudiants"