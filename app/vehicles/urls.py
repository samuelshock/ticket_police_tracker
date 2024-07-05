"""
Vehicles API urls.
"""
from django.urls import path
from vehicles import views

urlpatterns = [
    path('cargar_infraccion/',
         views.TicketCreateView.as_view(), name='create-ticket'),
    path('generar_informe/',
         views.ReportTicketView.as_view(), name='ticket-report'),
]
