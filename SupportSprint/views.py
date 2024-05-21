from django.contrib.auth.views import LoginView,LogoutView,PasswordChangeView
from .forms import CustomUserCreationForm 
from django.views.generic.edit import CreateView
from django.urls.base import reverse_lazy
from django.shortcuts import render



class MainLoginView(LoginView):
    template_name = 'login.html'

class MainPasswordChangeView(PasswordChangeView):
    template_name = 'password_change.html'
    
class MainLogoutView(LogoutView):
    template_name = 'logout.html'
    

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def main(request):
    return render(request, 'base.html')
