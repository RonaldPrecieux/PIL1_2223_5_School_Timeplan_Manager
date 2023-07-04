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
]


