from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

class Department(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Queue(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(
                                    Department,
                                    on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name



class Ticket(models.Model):
    STATUS_CHOICES = [
        ('Nowy', 'Nowy'),
        ('W trakcie', 'W trakcie'),
        ('Zakończony', 'Zakończony'),
        ('Zamknięty', 'Zamknięty'),
        ('Odrzucony', 'Odrzucony'),
        ('Zamrożony', 'Zamrożony'),
        ('Nieaktywny', 'Nieaktywny'),
    ]
    
    title = models.CharField(
                             default='Bez tytułu',
                             verbose_name='Tytuł zgłoszenia'
                             ,max_length=255
                             )
    reporter = models.CharField(
                            max_length=50,
                            verbose_name='Zgłaszający'
                            )
    content = models.TextField(
                            verbose_name = 'Treść',
                            max_length=10000
                            )
    owner = models.ForeignKey(
                            User,
                            blank=True, 
                            null=True, 
                            on_delete=models.CASCADE
                            )
    status = models.CharField(
                              max_length=20,
                              choices=STATUS_CHOICES,
                              default='Nowy'
                              )
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(
                              auto_now_add=True
                              )
    updated_at = models.DateTimeField(
                              auto_now=True
                              )
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

   
def update_ticket_updated_at(sender, instance, created, **kwargs):
    if created:
        instance.ticket.updated_at = timezone.now()
        instance.ticket.save()