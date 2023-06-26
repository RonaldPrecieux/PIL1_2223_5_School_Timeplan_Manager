

from django.contrib import admin
from django.urls import path, include
from showtimeplan import views
from EditTimeplan import views as app1

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',include('showtimeplan.urls')),
    path('',include('EditTimeplan.urls')),
]

   


