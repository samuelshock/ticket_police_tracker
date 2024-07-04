"""
Vehicles API urls.
"""
from django.urls import path
from vehicles.views import TicketCreateView

urlpatterns = [
    path('cargar_infraccion/',
         TicketCreateView.as_view(), name='create-ticket'),
]
