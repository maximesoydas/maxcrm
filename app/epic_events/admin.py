from django.contrib import admin
from epic_events.models import Client, Contract, ContractStatus, Event



# class ClientInline(admin.TabularInline):
#      model = Client
# Register your models here.
# @admin.register(Client)
# class GenericAdmin(admin.ModelAdmin):
#     pass

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display= ('first_name','last_name')
    # inlines = (ClientInline)
    
    
@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display= ('sales_contact','client','status')

@admin.register(ContractStatus)
class ContractStatusAdmin(admin.ModelAdmin):
    list_display= ('CHOICES',)
    
    
@admin.register(Event)
class Event(admin.ModelAdmin):
    list_display= ('client','support_contact','event_status')




