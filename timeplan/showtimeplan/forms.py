from django import forms
from showtimeplan.models import User

class UserForm(forms.ModelForm):
    email = forms.EmailField(
        error_messages={
            'unique': "Cet email est déjà utilisé. Veuillez en choisir un autre.",
        }
    )
    class Meta:
        model = User
        fields = ['nom', 'prenom', 'email', 'numero_telephone', 'mot_de_passe', 'confirmer_mot_de_passe']
