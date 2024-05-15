from django.contrib import admin

from django.contrib import admin
from .models import Ticket,Department,Queue,TicketResponse

admin.site.register(Ticket)
admin.site.register(Department)
admin.site.register(Queue)
admin.site.register(TicketResponse)

