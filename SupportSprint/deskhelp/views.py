from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.views.generic.edit import FormView, CreateView
from django.views.generic.base import View
from deskhelp.models import Ticket, Queue
from deskhelp.forms import SearchForm
from django.db.models import Q
from django.contrib import messages
from django.views.generic.base import TemplateView
from deskhelp.forms import TicketResponseForm, CreateTicketForm,CreateGuestTicketForm
from .models import TicketResponse,Department,Queue
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializer import TicketSerializer,TicketResponseSerializer,DepartmentSerializer,QueueSerializer



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
        context["user"] = self.request.user
        tickets = Ticket.objects.filter(
            status__in=[Ticket.Status.NOWY, Ticket.Status.W_TRAKCIE, Ticket.Status.ZAMROZONY]
        )
        for ticket in tickets:
            if len(ticket.title) > 40:
                ticket.truncated_title = ticket.title[:30] + "..."
            else:
                ticket.truncated_title = ticket.title
        context['tickets'] = tickets
        return context
    
class SearchTicketsView(FormView):
    template_name = 'tickets_search.html'
    form_class = SearchForm
    
    def form_valid(self, form):
        fraze = form.cleaned_data['fraze']
        tickets = Ticket.objects.filter(
            Q(id__icontains=fraze) |
            Q(title__icontains=fraze) |
            Q(reporter__icontains=fraze) |
            Q(owner__username__icontains=fraze) |
            Q(content__icontains=fraze)
        )

        for ticket in tickets:
            if len(ticket.title) > 35:
                ticket.truncated_title = ticket.title[:30] + "..."
            else:
                ticket.truncated_title = ticket.title

        return render(
            self.request,
            self.template_name,
            {
                'form': form,
                'tickets': tickets
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
    success_url = reverse_lazy('user_tickets')

    def form_valid(self, form):
        print("Form data:", form.cleaned_data) 
        form.instance.reporter = self.request.user.username
        return super().form_valid(form)


class CreateGuestTicketView(CreateView):
    form_class = CreateGuestTicketForm
    model = Ticket
    template_name = 'create_guest_ticket.html'
    success_url = reverse_lazy('guest_ticket')  

    def form_valid(self, form):
        response = super().form_valid(form)
        return HttpResponseRedirect(f"{self.success_url}?success=1")



class MainDeskView(FormView):
    template_name = 'desk_main.html'
    ################################################# sortowanie zrób od najnowszego dla kolejek ###############################################
    def get(self, request, *args, **kwargs):
        tickets = Ticket.objects.filter(
            owner=request.user
        ).exclude(
            status__in=[Ticket.Status.ZAMKNIETY, Ticket.Status.ODRZUCONY]
        )

        queues = get_user_queues(request.user)
        queues_tickets = {}
        for queue in queues:
            queues_tickets[queue] = Ticket.objects.filter(
                queue=queue
            ).exclude(
                status__in=[Ticket.Status.ZAMKNIETY, Ticket.Status.ODRZUCONY]
            )
        return render(
            request,
            self.template_name,
            {
                'tickets': tickets,
                'queues': queues,
                'queues_tickets': queues_tickets
            }
        )

class UserTicketsView(View):
    template_name = 'user_tickets.html'

    def get(self, request, *args, **kwargs):
        tickets = Ticket.objects.filter(
            reporter=request.user, 
        )

        for ticket in tickets:
            ticket.truncated_title = ticket.title[:30] + "..." if len(ticket.title) > 30 else ticket.title

        context = {
            "user": request.user,
            "tickets": tickets,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
 

def update_ticket(ticket_id, message_template, status=None):

    ticket = get_object_or_404(Ticket, pk=ticket_id)
    system_user = User.objects.get(username='System')
    message = message_template.format(user=str(ticket.owner or 'System'))
    TicketResponse.objects.create(ticket=ticket, author=system_user, body=message)
    
    ticket.updated_at = timezone.now()
    if status:
        ticket.status = status
        ticket.save()
    
def accept_ticket(request, ticket_id, action_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    valid_statuses = {status: label for status, label in Ticket.Status.choices}

    if action_id not in valid_statuses:
        messages.error(request, f"Nieprawidłowa akcja: {action_id}")
        return redirect(reverse('ticket_details', kwargs={'ticket_id': ticket_id}))

    status_messages = {
        Ticket.Status.W_TRAKCIE: f"Użytkownik {request.user} przyjął zgłoszenie.",
        Ticket.Status.ODRZUCONY: f"Użytkownik {request.user} odrzucił zgłoszenie.",
        Ticket.Status.ZAKONCZONY: f"Zgłoszenie zostało oznaczone jako zakończone przez {request.user}.",
        Ticket.Status.NOWY: f"Zgłoszenie zostało przywrócone do statusu nowego przez {request.user}.",
    }

    if ticket.status in [Ticket.Status.NOWY, Ticket.Status.ODRZUCONY]:
        ticket.owner = request.user
        update_ticket(ticket_id, status_messages[Ticket.Status.W_TRAKCIE], Ticket.Status.W_TRAKCIE)
        messages.success(request, f"Użytkownik {request.user} przyjął zgłoszenie.")
        ticket.save()
        return redirect(reverse('ticket_details', kwargs={'ticket_id': ticket_id}))

    if action_id == Ticket.Status.ODRZUCONY:
        ticket.owner = None

        update_ticket(ticket_id, status_messages[Ticket.Status.ODRZUCONY], Ticket.Status.ODRZUCONY)
        messages.success(request, "Zgłoszenie zostało odrzucone.")
        ticket.save()
        return redirect(reverse('ticket_details', kwargs={'ticket_id': ticket_id}))

    if ticket.owner == request.user:
        update_ticket(ticket_id, status_messages.get(action_id, f"Status zmieniony na {valid_statuses[action_id]}."), action_id)
        messages.success(request, f"Zgłoszenie oznaczone jako {valid_statuses[action_id]}.")
    else:
        messages.warning(request, "Tylko właściciel zgłoszenia może zmieniać status.")

    return redirect(reverse('ticket_details', kwargs={'ticket_id': ticket_id}))