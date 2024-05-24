from django.urls import path
from .views import ListTickets, TicketDetailsView, accept_ticket, CreateTicketView

urlpatterns = [
    path("", ListTickets.as_view(), name='ticket-list'),
    path('ticket/<int:ticket_id>/', TicketDetailsView.as_view(), name='ticket_details'),
    path('ticket/<int:ticket_id>/accept/', accept_ticket, name='accept_ticket'),
    path('search/', ListTickets.as_view(), name='search_tickets'),
    path('create/', CreateTicketView.as_view(), name='create_ticket'),
]