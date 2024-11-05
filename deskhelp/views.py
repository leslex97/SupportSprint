from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic.edit import FormView, CreateView
from django.views.generic.base import View
from deskhelp.models import Ticket, Queue
from deskhelp.forms import SearchForm
from django.db.models import Q
from django.contrib import messages
from django.views.generic.base import TemplateView
from deskhelp.forms import TicketResponseForm, CreateTicketForm
from .models import TicketResponse,Department,Queue
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializer import TicketSerializer,TicketResponseSerializer,DepartmentSerializer,QueueSerializer

############################# TEST API ###############################
class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class TicketResponseViewSet(viewsets.ModelViewSet):
    queryset = TicketResponse.objects.all()
    serializer_class = TicketResponseSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
        
class QueueViewSet(viewsets.ModelViewSet):
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer
########################################################

def get_user_queues(user):
    if user.is_authenticated:
        return Queue.objects.filter(users=user)
    return []


class ListTickets(
    FormView
):
    template_name = 'tickets.html'
    form_class = SearchForm
    success_url ='.'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tickets'] = Ticket.objects.all()
        return context
    
    def form_valid(self, form):
        tickets=Ticket.objects.filter(
           Q(id__icontains=form.cleaned_data['fraze'])|
        Q(title__icontains=form.cleaned_data['fraze']) |
        Q(reporter__icontains=form.cleaned_data['fraze'])|
        Q(content__icontains=form.cleaned_data['fraze'])
        )
        return render(
            request=self.request,
            template_name=self.template_name,
            context={
                'form': form,
                'tickets':tickets
            }
        )
        
class TicketDetailsView(LoginRequiredMixin, TemplateView):
    template_name = 'ticket.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket_id = self.kwargs["ticket_id"]
        ticket = Ticket.objects.get(pk=ticket_id)
        responses = ticket.responses.all()  
        context["ticket"] = ticket
        context["response_form"] = TicketResponseForm()
        context["responses"] = responses
        context["user"] = self.request.user
        context['nobody'] = User.objects.get(username ='nobody')
        return context

    def post(self, request, *args, **kwargs):
        ticket_id = self.kwargs["ticket_id"]
        ticket = Ticket.objects.get(pk=ticket_id)
        response_form = TicketResponseForm(request.POST)

        if response_form.is_valid():
            response = response_form.cleaned_data['response']
            TicketResponse.objects.create(ticket=ticket, author=request.user, body=response)
            ticket.updated_at = timezone.now()
            ticket.save()
            return redirect('ticket_details', ticket_id=ticket_id)
        
        return render(request, self.template_name, {'ticket': ticket,  'response_form': response_form})

class CreateTicketView(CreateView):
    form_class = CreateTicketForm
    model = Ticket
    template_name = 'create_ticket.html'
    success_url = reverse_lazy('ticket-list')
    
    def form_valid(self, form):
        form.instance.reporter = self.request.user.username
        return super().form_valid(form)

class UserTicketsView(View):
    template_name = 'desk_main.html'
    def get(self, request, *args, **kwargs):
        tickets = Ticket.objects.filter(owner=request.user)
        queues = get_user_queues(request.user)
        queues_tickets = {}
        for queue in queues:
            queues_tickets[queue]=(Ticket.objects.filter(queue=queue))
        return render(request, self.template_name, {'tickets': tickets,
                                                    'queues': queues,
                                                    'queues_tickets':queues_tickets})


def update_ticket(ticket_id, action, status):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    system_user = User.objects.get(username='System')
    TicketResponse.objects.create(ticket = ticket, author = system_user, body = action)
    ticket.updated_at = timezone.now()
    ticket.status = status
    
def accept_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if request.user != ticket.owner:
        ticket.owner = request.user
        update_ticket(ticket_id, f'Użytkownik {request.user} Przyjął zgłoszenie', 'W trakcie')
        ticket.save()
        messages.success(request, 'Pomyślnie przyjęto zgłoszenie.')
    else:
        messages.info(request, 'Jesteś już właścicielem tego zgłoszenia.')

    return redirect(reverse('ticket_details', kwargs={'ticket_id': ticket_id}))