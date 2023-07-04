from django.urls import path
from . import views as app1

urlpatterns= [
    path('dashboardAdmin/<int:label>/',app1.dashboardAdmin,name="dashboardAdmin"),
    path('modifydef/',app1.Modify,name="modify_url"),
    path('save_cours/', app1.save_cours, name='save_cours'),
    path('DeleteCours/<int:id>/',app1.DeleteCours,name="DeleteCours"),
    path('copier_table/', app1.copier_table, name='copier_table'),
    path('save_coursAll/',app1.save_coursAll,name="save_coursAll"),
    path('ModifyAll/',app1.ModifyAll,name='ModifyAll'),
    path('DeleteCoursAll/<int:id>/',app1.DeleteCoursAll,name="DeleteCoursAll"),
     path('copier_table/', app1.copier_table, name='copier_table'),
    path('ajouter_cours/', app1.ajouter_cours, name='ajouter_cours'),
    path('definir_matiere/', app1.definir_matiere, name='definir_matiere'),
    path('modifier_matiere/', app1.modifier_matiere, name='modifier_matiere'),
    path('supprimer_matiere/', app1.supprimer_matiere, name='supprimer_matiere'),
]


