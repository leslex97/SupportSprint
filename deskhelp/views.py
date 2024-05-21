from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic.edit import FormView
from deskhelp.models import Ticket
from deskhelp.forms import SearchForm
from django.db.models import Q
from django.views.generic.base import TemplateView
from deskhelp.forms import TicketResponseForm
from .models import TicketResponse
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

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
        
        return render(request, self.template_name, {'ticket': ticket, 'response_form': response_form})