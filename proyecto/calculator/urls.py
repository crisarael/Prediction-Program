from django.urls import path
from calculator import views

app_name = "calculator"

urlpatterns = [
    # url para comunicacion con la aplicacion
    path('recibir/', views.lista.as_view(), name="reciv"),
]
