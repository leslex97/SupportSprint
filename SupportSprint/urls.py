"""
URL configuration for SupportSprint project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views


from django.contrib.auth.views import LogoutView, PasswordChangeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('deskhelp.urls')),
    path('login/', views.MainLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_change/', PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('password_change/done/', PasswordChangeView.as_view(template_name='password_change_done.html')),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('user_details/<str:username>/', views.UserDetailsView.as_view(), name='user_details'),
    path('edit_user_details/<str:username>/', views.EditUserInfoView.as_view(), name='edit_user'),
    path('api/', include('api.urls'))
]