from django.urls import path
from . import views as app1

urlpatterns= [
    path('dashboardAdmin/',app1.dashboardAdmin,name="dashboardAdmin"),


    path('save_cours/', app1.save_cours, name='save_cours'),
]


