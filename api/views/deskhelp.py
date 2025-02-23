from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from deskhelp.models import Ticket, TicketResponse, Queue, Department
from api.serializers.deskhelp import (
    TicketSerializer, TicketResponseSerializer, QueueSerializer, DepartmentSerializer
)
from api.serializers.supportsprint import UserSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from api.serializers.deskhelp import ChangePasswordSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class QueueViewSet(viewsets.ModelViewSet):
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer

    @action(detail=True, methods=['get'])
    def users(self, request, pk=None):
        queue = self.get_object()
        users = queue.users.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    @action(detail=True, methods=['get'], url_path='details')
    def ticket_with_responses(self, request, pk=None):
        ticket = self.get_object()
        responses = TicketResponse.objects.filter(ticket=ticket)
        ticket_data = self.get_serializer(ticket).data
        response_serializer = TicketResponseSerializer(responses, many=True)
        return Response({"ticket": ticket_data, "responses": response_serializer.data})

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user.username)

    @action(detail=True, methods=['patch'], url_path='change-status')
    def change_status(self, request, pk=None):
        ticket = self.get_object()
        new_status = request.data.get('status')

        valid_statuses = [choice[0] for choice in Ticket.Status.choices]
        if new_status not in valid_statuses:
            return Response({"error": f"Invalid status. Valid statuses are: {valid_statuses}"}, status=status.HTTP_400_BAD_REQUEST)

        ticket.status = new_status
        ticket.owner = request.user
        ticket.save()

        return Response({"message": "Status and owner updated successfully", "new_status": ticket.status, "new_owner": ticket.owner.username})

class TicketResponseViewSet(viewsets.ModelViewSet):
    queryset = TicketResponse.objects.all()
    serializer_class = TicketResponseSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='by-ticket')
    def get_responses_by_ticket(self, request):
        ticket_id = request.query_params.get('ticket_id')
        if not ticket_id:
            return Response({"error": "ticket_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)

        responses = TicketResponse.objects.filter(ticket=ticket)
        serializer = TicketResponseSerializer(responses, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ReporterTicketsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer

    def get_queryset(self):
        return Ticket.objects.filter(reporter=self.request.user.username)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.validated_data["old_password"]):
                return Response({"old_password": "Stare hasło jest niepoprawne."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.validated_data["new_password1"])
            user.save()

            return Response({"message": "Hasło zostało zmienione."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)