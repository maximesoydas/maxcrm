from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
import uuid
class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    date_create = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'groups__name': "sales"})
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
class Contract(models.Model):
    SIGNED = 'signed'
    PENDING = 'pending'
    FINISHED = 'finished'

    CHOICES = (
        (SIGNED, 'Signed'),
        (PENDING, 'Pending'),
        (FINISHED, 'Finished'),
    )
    sales_contact = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255, choices=CHOICES, default=PENDING)
    amount = models.FloatField()
    payment_due = models.DateField()
    
    
class ContractStatus(models.Model):
    SIGNED = 'signed'
    PENDING = 'pending'
    FINISHED = 'finished'

    CHOICES = (
        (SIGNED, 'Signed'),
        (PENDING, 'Pending'),
        (FINISHED, 'Finished'),
    )
    id = models.AutoField(primary_key=True, editable=False)
    status = models.CharField(max_length=255, choices=CHOICES, default=PENDING)
    
    def __str__(self):
        return str(self.id) + ' ' + str(self.status)

class Event(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)
    support_contact = models.ForeignKey(User,blank=True, null=True, on_delete=models.CASCADE, limit_choices_to={'groups__name': "support"})
    event_status = models.ForeignKey(ContractStatus, on_delete=models.CASCADE)
    attendees = models.IntegerField()
    event_date = models.DateTimeField()
    notes = models.TextField(blank=True)
    