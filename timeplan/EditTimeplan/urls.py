from django.urls import path
from . import views as app1

urlpatterns= [
    path('dashboardAdmin/<int:label>/',app1.dashboardAdmin,name="dashboardAdmin"),
    path('modifydef/',app1.Modify,name="modify_url"),
    path('save_cours/', app1.save_cours, name='save_cours'),
    path('DeleteCours/<int:id>/',app1.DeleteCours,name="DeleteCours"),
     path('copier_table/', app1.copier_table, name='copier_table'),
]


