from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Department(models.Model):
    name = models.CharField(max_length=100)
    users = models.ForeignKey(User , on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.name

class Queue(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='queues')
    
    def __str__(self):
        return f"{self.name} - {self.department.name}"

class Ticket(models.Model):
    class Status(models.TextChoices):
        NOWY = 'Nowy', _('Nowy')
        W_TRAKCIE = 'W trakcie', _('W trakcie')
        ZAKONCZONY = 'Zakończony', _('Zakończony')
        ZAMKNIETY = 'Zamknięty', _('Zamknięty')
        ODRZUCONY = 'Odrzucony', _('Odrzucony')
        ZAMROZONY = 'Zamrożony', _('Zamrożony')
        NIEAKTYWNY = 'Nieaktywny', _('Nieaktywny')
        
    title = models.TextField(
        default='Bez tytułu',
        verbose_name='Tytuł zgłoszenia',
        null=False
    )
    reporter = models.CharField(
        max_length=50,
        verbose_name='Zgłaszający'
    )
    content = models.TextField(
        verbose_name='Treść',
        max_length=10000,
        null=False
    )
    owner = models.ForeignKey(
        User,
        blank=True, 
        null=True, 
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NOWY
    )
    queue = models.ForeignKey(Queue,
                               on_delete=models.CASCADE,
                                 default=1,
                                 verbose_name='Kolejka')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.owner:
            self.owner = User.objects.get(username='nobody')
        super().save(*args, **kwargs)
    
    def owner_display(self):
        return self.owner.username if self.owner else 'nobody'
    
    def __str__(self):
        return self.title

class TicketResponse(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        related_name='responses',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to Ticket #{self.ticket.id} by {self.author.username}"

@receiver(post_save, sender=TicketResponse)
def update_ticket_updated_at(sender, instance, created, **kwargs):
    if created:
        instance.ticket.updated_at = timezone.now()
        instance.ticket.save()

# Nowy sygnał do automatycznego przypisywania kolejek do departamentu
@receiver(post_save, sender=Department)
def assign_queues_to_department(sender, instance, created, **kwargs):
    if created:

        queues = Queue.objects.all()
        for queue in queues:
            queue.department = instance
            queue.save()