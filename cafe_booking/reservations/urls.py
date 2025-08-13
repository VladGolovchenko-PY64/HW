from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tables/', views.tables_list, name='tables_list'),
    path('reservations/new/', views.new_reservation, name='new_reservation'),
    path('reservations/my/', views.my_reservations, name='my_reservations'),
]
