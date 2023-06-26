from django.urls import path
from . import views as app1

urlpatterns= [
    path('dashboardAdmin/',app1.dashboardAdmin,name="dashboardAdmin"),
    path('modifydef/',app1.Modify,name="modify_url"),
    path('save_cours/', app1.save_cours, name='save_cours'),
   # path('dashboardAdmin/<object:CoursProgrammer>',app1.dashboardAdmin,name="dashboardAdmin_redirect"),
]


