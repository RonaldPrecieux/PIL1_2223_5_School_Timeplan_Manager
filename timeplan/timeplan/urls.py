
from django.contrib import admin
from django.urls import path
from showtimeplan import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("insertuser/", views.insertuser, name="insertuser"),
    path("", views.index, name ="accueil"), 
    path("login/", views.login, name = "login"), # C'est la page de connexion
    path("register/", views.register, name="register"), #Page d'inscription
    path("bienvenue/<str:prenom>/", views.bienvenue, name ="bienvenue"),#Page temporaire
    path("bienvenue_connexion/<str:prenom>/", views.bienvenue_connexion, name="bienvenue_connexion"),#Page temporaire de connexion
    path("mot_de_passe_oublie/", views.mot_de_passe_oublie, name = "mot_de_passe_oublie"),
    path('reinit_mot_de_passe/<int:id>/', views.afficher_page_reinit_mot_de_passe, name='afficher_page_reinit_mot_de_passe'),
    path('traiter_reinit_mot_de_passe/<int:id>/', views.traiter_reinit_mot_de_passe, name='traiter_reinit_mot_de_passe'),
    path("bienvenue_recuperation/<str:prenom>/", views.bienvenue_recuperation, name="bienvenue_recuperation"),
    ]
