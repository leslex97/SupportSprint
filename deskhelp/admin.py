from django.contrib import admin
from .models import Department, Queue, Ticket, TicketResponse

class QueueAdmin(admin.ModelAdmin):
    list_display = ['name', 'department']
    filter_horizontal = ['users']

admin.site.register(Department)
admin.site.register(Queue, QueueAdmin)
admin.site.register(Ticket)
admin.site.register(TicketResponse)