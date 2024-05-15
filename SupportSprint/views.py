from django.contrib.auth.views import LoginView,PasswordChangeView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls.base import reverse_lazy
from django.shortcuts import render

def main(request):
    return render(request, 'base.html')
