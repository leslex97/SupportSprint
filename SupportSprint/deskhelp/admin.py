from django.contrib import admin
from .models import Department, Queue, Ticket, TicketResponse
from SupportSprint.models import UserProfile

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'assigned_user']
    search_fields = ['name']

    def assigned_user(self, obj):
        if obj.users:
            return obj.users.username
        else:
            return "Brak przypisanego użytkownika"
        
    assigned_user.short_description = "Przypisany użytkownik"

admin.site.register(Department, DepartmentAdmin)


class QueueAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'display_users']
    list_filter = ['department']
    search_fields = ['name']
    filter_horizontal = ['users']

    def display_users(self, obj):
        users_list = []
        for user in obj.users.all():
            users_list.append(user.username)

        if len(users_list) > 0:
            return ", ".join(users_list)
        else:
            return "Brak przypisanych użytkowników"

    display_users.short_description = "Przypisani użytkownicy"

admin.site.register(Queue, QueueAdmin)



class TicketResponseInline(admin.TabularInline):
    model = TicketResponse
    extra = 1  

class TicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'reporter', 'queue', 'owner_display', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'queue', 'reporter']
    search_fields = ['title', 'content', 'reporter', 'owner__username']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    inlines = [TicketResponseInline]  

    def owner_display(self, obj):
        if obj.owner:
            return obj.owner.username
        else:
            return 'nobody'

    owner_display.short_description = "Właściciel"
admin.site.register(Ticket, TicketAdmin)

class TicketResponseAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'author', 'created_at', 'body_preview']
    list_filter = ['author']
    search_fields = ['body', 'author__username']
    readonly_fields = ['created_at']

    def body_preview(self, obj):
        if len(obj.body) > 50:
            return obj.body[:50] + "..."
        else:
            return obj.body

    body_preview.short_description = "Treść odpowiedzi"

admin.site.register(TicketResponse, TicketResponseAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number']
    search_fields = ['user__username', 'phone_number']

admin.site.register(UserProfile, UserProfileAdmin)