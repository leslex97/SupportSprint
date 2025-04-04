from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.supportsprint import UserViewSet, UserProfileViewSet, CurrentUserView
from api.views.deskhelp import ReporterTicketsView, TicketViewSet, TicketResponseViewSet, QueueViewSet, DepartmentViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views.deskhelp import ChangePasswordView


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'user-profiles', UserProfileViewSet, basename='user-profiles')
router.register(r'tickets', TicketViewSet, basename='tickets')
router.register(r'responses', TicketResponseViewSet, basename='responses')
router.register(r'queues', QueueViewSet, basename='queues')
router.register(r'departments', DepartmentViewSet, basename='departments')

urlpatterns = [
    path('users/me/', CurrentUserView.as_view(), name='current_user'),
     path('change-password/', ChangePasswordView.as_view(), name='change_password'),    
     path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('tickets/reporter/', ReporterTicketsView.as_view(), name='reporter_tickets'),
    path('', include(router.urls)),
]
