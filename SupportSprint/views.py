from django.contrib.auth.views import LoginView,LogoutView
from django.views import View
from .forms import CustomUserCreationForm
from django.views.generic.edit import CreateView
from django.urls.base import reverse_lazy
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import UserForm, UserProfileForm
from deskhelp.views import get_user_queues
from rest_framework import viewsets
from .serializer import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class MainLoginView(LoginView):
    template_name = 'login.html'

 
class MainLogoutView(LogoutView):
    template_name = 'logout.html'

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class UserDetailsView(View):
    template_name = 'user_details.html'
    success_url = reverse_lazy('tickets')
    
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        profile = user.userprofile
        
        return render(request, self.template_name, {'user': user,
                                                    'queues': get_user_queues(request.user), 
                                                    'profile': profile})
class EditUserInfoView(View):
    def get(self, request, *args, **kwargs):
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)
        return render(request, 'edit_user_info.html', {
            'user':request.user,
            'user_form': user_form,
            'profile_form': profile_form
        })

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(reverse_lazy(
                                        'user_details', 
                                         kwargs={'username': request.user.username}))

        return render(request, 'edit_user_info.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })
    
