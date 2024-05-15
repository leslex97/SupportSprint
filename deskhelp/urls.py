from django.urls import path
from .views import ListTickets,TicketDetailsView


urlpatterns = [
    path("", ListTickets.as_view(), name= 'ticket-list' ),
        path('ticket/<int:ticket_id>/', TicketDetailsView.as_view(), name='ticket_details'),
]
