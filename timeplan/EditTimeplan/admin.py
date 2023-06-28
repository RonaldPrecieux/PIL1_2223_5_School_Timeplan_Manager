from django.contrib import admin
from EditTimeplan.models import AdminUser,Matiere
from django.contrib.auth.hashers import make_password

class AdminUserAdmin(admin.ModelAdmin):
    exclude = ('Code_confirmation',)
    def save_model(self, request, obj, form, change):
        # Hacher le mot de passe avant de l'enregistrer
        
        obj.mot_de_passe = make_password(obj.mot_de_passe)
        super().save_model(request, obj, form, change)
admin.site.register(AdminUser, AdminUserAdmin)
    

class Matiere(admin.ModelAdmin):
    list_display = ('nom','enseignant','timing','informations') # liste les champs que nous voulons sur l'affichage de la liste
    admin.site.register(Matiere)#Comment ca marche?


# Register your models here.
    