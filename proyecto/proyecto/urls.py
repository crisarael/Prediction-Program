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
from rest_framework.authtoken import views as view


urlpatterns = [
    # Url de la aplicacion calculadora
    path('calculator/', include('calculator.urls', namespace="calculator")),
    path('admin/', admin.site.urls),
    # Url de Index
    path('', views.Index.as_view(), name='Index'),
    # Crud
    path('upload', views.uploadcsv, name='Upload'),
    path('detail/<int:pk>', views.DetailCsv.as_view(), name='Detail'),
    path('detailedit/<int:pk>', views.editarModelo, name='Detaile'),
    path('borrar/<int:pk>', views.BorrarCsv.as_view(), name="Delete"),
    # Urls para compartir tabla
    path('share/<int:pk>', views.CompartirCsv.as_view(), name='Share'),
    path('mip/<int:pk>', views.HacerPublico.as_view(), name='MakeItPublic'),
    # Api que retorna un json de la tabla
    path('tablajson/<int:pk>', views.lista, name="jsontab"),
    path('jsonget/<int:pk>', views.listaPublica, name="jsonget"),
    # Api que elimina un registro
    path('eliminar/<int:pk>', views.eliminarLista, name="recive"),
    # Api que muestra los registros de un usuariopara
    path('ver/', views.verModelo.as_view(), name="apisee"),
    # Url de formulario para graficar
    path('graficarform/<int:pk>', views.graficar, name="graf"),
    # Url de prueba
    path('hijo/<int:pk>', views.subData, name="sub"),
    # Urls de autentificacion
    path('login/', auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="login.html"), name="logout"),
    path('registrarusuario/', views.RegistrarUsuario, name='regU'),
    # Obtencion de token de seguridad
    path('api-token-auth/', view.obtain_auth_token),
    # Descargar csv_file
    path('dwcsv/<int:pk>', views.descargarCsv, name="dwcsv"),
    path('dwcsvp/<int:pk>', views.descargarCsvP, name="dwcsvP"),


]
