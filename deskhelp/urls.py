from django.urls import path, include
from .views import ListTickets,UserTicketsView, TicketDetailsView, accept_ticket, CreateTicketView,TicketViewSet,TicketResponseViewSet, QueueViewSet, DepartmentViewSet
from rest_framework import routers
from SupportSprint.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)  
router.register(r'tickets', TicketViewSet)
router.register(r'tickets-responses', TicketResponseViewSet)
router.register(r'queues', QueueViewSet)
router.register(r'departments', DepartmentViewSet)


urlpatterns = [
    path("", UserTicketsView.as_view(), name='home'),
    path('tickets/', ListTickets.as_view(), name='tickets'),
    path('ticket/<int:ticket_id>/', TicketDetailsView.as_view(), name='ticket_details'),
    path('ticket/<int:ticket_id>/accept/', accept_ticket, name='accept_ticket'),
    path('search/', ListTickets.as_view(), name='search_tickets'),
    path('create/', CreateTicketView.as_view(), name='create_ticket'),
    path('api/', include(router.urls)),
    path('api-auth', include('rest_framework.urls', namespace='rest_framefork')),
]