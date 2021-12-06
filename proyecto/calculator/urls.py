from django.urls import path
from calculator import views

app_name = "calculator"

urlpatterns = [
    # url para comunicacion con la aplicacion
    path('recibir/<int:pk>', views.lista.as_view(), name="reciv"),
    path('graficar/', views.grafica.as_view(), name="reciv"),
]
