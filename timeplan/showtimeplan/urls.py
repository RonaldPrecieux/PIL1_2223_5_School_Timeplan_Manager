from django.urls import path
from EditTimeplan import views as app1
from . import views

from django.contrib import admin


urlpatterns = [
    path("", views.index, name="accueil"),
    path("login/", views.login, name="login"),
    path("insertuser/", views.insertuser, name="insertuser"),
    path('dashboard/', views.dashboardStudent, name="dashboardStudent"),
    path("register/", views.register, name="register"),
    path("dashboardAdmin/", app1.dashboardAdmin, name="dashboardAdmin"),
    path("mot_de_passe_oublie/", views.mot_de_passe_oublie, name="mot_de_passe_oublie"),
    path('reinit_mot_de_passe/<int:id>/', views.afficher_page_reinit_mot_de_passe, name='afficher_page_reinit_mot_de_passe'),
    path('traiter_reinit_mot_de_passe/<int:id>/', views.traiter_reinit_mot_de_passe, name='traiter_reinit_mot_de_passe'),
    path("bienvenue_recuperation/<str:prenom>/", views.bienvenue_recuperation, name="bienvenue_recuperation"),
]