from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nazwa użytkownika'})
        self.fields['username'].label = 'Nazwa użytkownika'
        self.fields['username'].help_text = None
        
        
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Hasło'})
        self.fields['password1'].label = 'Hasło'
        self.fields['password1'].help_text = None
        
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Potwierdzenie hasła'})
        self.fields['password1'].label = "Powtórz Hasło"
        self.fields['password2'].help_text = None
 