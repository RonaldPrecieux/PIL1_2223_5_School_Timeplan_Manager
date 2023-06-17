from django import forms
from .models import User
from django.core.exceptions import ValidationError
class UserForm(forms.ModelForm):
    mot_de_passe = forms.CharField(widget=forms.PasswordInput)
    confirmer_mot_de_passe = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['nom', 'prenom', 'email', 'numero_telephone', 'mot_de_passe', 'confirmer_mot_de_passe']


    
    