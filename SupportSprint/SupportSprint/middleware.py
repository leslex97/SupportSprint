from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        exempt_urls = [
            reverse('login'),  
            reverse('signup'), 
            reverse('logout'),
            reverse('guest_ticket')

        ]

        # Dopuszczenie wszystkich ścieżek API do wyjątków
        if request.path.startswith('/api/'):
            return self.get_response(request)

        # Sprawdzanie, czy użytkownik jest uwierzytelniony
        if not request.user.is_authenticated and request.path not in exempt_urls:
            return redirect(settings.LOGIN_URL)

        response = self.get_response(request)
        return response