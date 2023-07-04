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
    


# Register your models here.
    