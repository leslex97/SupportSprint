from django import forms
from deskhelp.models import Ticket
from .models import TicketResponse

class SearchForm(forms.Form):
    fraze = forms.CharField(
        required=False,
        strip=True,
        max_length=20,
        label = 'Wyszukiwanie')
    
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = "__all__"
        
class TicketResponseForm(forms.Form):
    response = forms.CharField(widget=forms.Textarea,
                               label = 'Odpowiedz')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

class CreateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title','content', 'queue']

class CreateGuestTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title','content', 'queue', 'reporter']

        
