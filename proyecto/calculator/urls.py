from django.urls import path
from calculator import views

app_name = "calculator"

urlpatterns = [
    # De prueba que retorna una tabla modificada como hijo(En construccion)
    path('recibir/<int:pk>', views.lista.as_view(), name="reciv"),
    # Url que grafica
    path('graficar/', views.grafica.as_view(), name="graf"),
]
