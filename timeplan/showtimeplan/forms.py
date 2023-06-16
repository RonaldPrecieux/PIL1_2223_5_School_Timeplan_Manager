from django import forms
from .models import User

class UserForm(forms.ModelForm):
    mot_de_passe = forms.CharField(widget=forms.PasswordInput)
    confirmer_mot_de_passe = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['nom', 'prenom', 'email', 'numero_telephone', 'mot_de_passe', 'confirmer_mot_de_passe']
    
    def clean(self):
        cleaned_data = super().clean()
        mot_de_passe = cleaned_data.get('mot_de_passe')
        confirmer_mot_de_passe = cleaned_data.get('confirmer_mot_de_passe')

        if mot_de_passe and confirmer_mot_de_passe and mot_de_passe != confirmer_mot_de_passe:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")