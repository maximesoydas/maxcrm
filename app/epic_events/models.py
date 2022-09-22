from django.db import models
from django.contrib.auth.models import User
# Create your models here.

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
    
class Contract(models.Model):
    sales_contact = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField()
    amount = models.FloatField()
    payment_due = models.DateTimeField()
    
    
class ContractStatus(models.Model):
    OK = 'ok'
    PENDING = 'pending'
    FAILED = 'failed'

    CHOICES = (
        (OK, 'Ok'),
        (PENDING, 'Pending'),
        (FAILED, 'Failed'),
    )

    status = models.CharField(max_length=255, choices=CHOICES, default=PENDING)
    
class Event(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)
    support_contact = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': "support"})
    event_status = models.ForeignKey(ContractStatus, on_delete=models.CASCADE)
    attendees = models.IntegerField()
    event_date = models.DateTimeField()
    notes = models.TextField(blank=True)
    