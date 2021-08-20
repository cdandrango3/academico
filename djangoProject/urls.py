"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from djangoProject.academico.views import c
from djangoProject.academico.views import login
from djangoProject.academico.views import logout
from djangoProject.academico.views import perfil
from djangoProject.academico.views import elegir_curso
from djangoProject.academico.views import editar_curso
#from django.contrib.auth import login
from djangoProject.academico.views import allprofe

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',c),
    path('login/',login),
    path('profesores',allprofe),
    path('logout/',logout),
    path('perfil/',perfil),
    path('curso/',elegir_curso),
    path('editar/<str:materias>',editar_curso,name="editar")
    #path('login/',login,{'template_name':'login.html'}, name='login'),
]
