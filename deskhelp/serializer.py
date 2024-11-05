from .models import Department, Queue, Ticket, TicketResponse
from rest_framework import serializers



class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Department
        fields = ['name', 'users']
class QueueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Queue
        fields = ['name', 'department', 'users']

class TicketSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Ticket
        fields = ['title', 'reporter', 'content', 'owner', 'status', 'queue', 'created_at','updated_at']
class TicketResponseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=TicketResponse
        fields = ['ticket', 'author', 'body', 'created_at']