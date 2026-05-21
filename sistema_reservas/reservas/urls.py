from django.urls import path
from . import views

urlpatterns = [
    path('', views.painel, name='painel'),
    path('reservas/<int:reserva_id>/cancelar/', views.cancelar_reserva, name='cancelar_reserva'),
]
