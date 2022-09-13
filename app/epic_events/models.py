from django.db import models

# Create your models here.
class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    date_create = models.DateTimeField()
    date_updated = models.DateTimeField()
    sales_contact = models.CharField(max_length=100)