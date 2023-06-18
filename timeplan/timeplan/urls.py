"""
URL configuration for timeplan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
    path("search_acount/", views.cherche_le_compte,name="trouver_mon_compte")
]