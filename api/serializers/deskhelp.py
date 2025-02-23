from rest_framework import serializers
from deskhelp.models import Ticket, TicketResponse, Queue, Department
from django.contrib.auth.models import User


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'users']

class QueueSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    
    class Meta:
        model = Queue
        fields = ['id', 'name', 'department', 'users']

class TicketSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    queue_name = serializers.CharField(source='queue.name', read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'reporter', 'content', 'owner', 'owner_username',
            'status', 'queue', 'queue_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'owner', 'created_at', 'updated_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['status_choices'] = [choice[0] for choice in Ticket.Status.choices]
        return representation

class TicketResponseSerializer(serializers.ModelSerializer):
    ticket = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all())  
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = TicketResponse
        fields = ['id', 'ticket', 'author', 'author_username', 'body', 'created_at']
        read_only_fields = ['id', 'author', 'author_username', 'created_at']

    def validate_body(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Treść odpowiedzi musi mieć co najmniej 5 znaków.")
        return value

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password1 = serializers.CharField(required=True, write_only=True)
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        if data["new_password1"] != data["new_password2"]:
            raise serializers.ValidationError({"new_password2": "Nowe hasła nie są identyczne."})
        return data