"""proyecto URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from inicio import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('calculator/', include('calculator.urls', namespace="calculator")),
    path('admin/', admin.site.urls),
    # Url de Index
    path('', views.Index.as_view(), name='Index'),
    path('upload', views.uploadcsv, name='Upload'),
    path('detail/<int:pk>', views.DetailCsv.as_view(), name='Detail'),
    path('share/<int:pk>', views.CompartirCsv.as_view(), name='Share'),
    path('mip/<int:pk>', views.HacerPublico.as_view(), name='MakeItPublic'),
    path('borrar/<int:pk>', views.BorrarCsv.as_view(), name="Delete"),
    path('tablajson/<int:pk>', views.lista, name="reciv"),
    # Url para el Crud de Exchange
    path('registrarusuario/', views.RegistrarUsuario, name='regU'),
    # Urls de autentificacion
    path('login/', auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="login.html"), name="logout"),

]
