from django.contrib import admin
from epic_events.models import Client, Contract, ContractStatus, Event
from django.db.models import Q

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display= ('first_name','last_name')

    def get_queryset(self, request):
        self.request = request
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset.all()

        if request.user.groups.filter(name='sales'):
            # return only clients related to the salesman/saleswoman
            return queryset.filter(sales_contact=self.request.user.id)
        if request.user.groups.filter(name='support'):
            # return only clients related to the event 'supported' by the user
            return queryset.filter(event__support_contact=self.request.user.id)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
            if db_field.name == 'sales_contact':
                kwargs['initial'] = request.user.id
                kwargs['disabled'] = True
                # field = db_field
                
               
                return db_field.formfield(**kwargs)
            return super(ClientAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    # exclude = ("sales_contact",)
    # readonly_fields=('sales_contact', )

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display= ('id','sales_contact','client','status',)
    # readonly_fields = ('id',)


    # List Contracts
    def get_queryset(self, request):
        self.request = request
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset.all()

        if request.user.groups.filter(name='sales'):
            # return only clients related to the salesman/saleswoman
            return queryset.filter(sales_contact=self.request.user.id)

    # Create/Update Contracts
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'sales_contact':
            kwargs['initial'] = request.user.id
            kwargs['disabled'] = True
            return db_field.formfield(**kwargs)
        if db_field.name == 'client':
            # print(kwargs['limit'])
            
            kwargs['limit_choices_to'] ={'sales_contact_id': request.user.id}  
        return super(ContractAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        
    def save_model(self, request, obj, form, change) -> None: 
        super().save_model(request, obj, form, change)
        print('testtesttests')
        print(obj.id)
        cs = ContractStatus(id=obj.id, status = str(obj.status))
        cs.save()

        return super().save_model(request, obj, form, change)

@admin.register(ContractStatus)
class ContractStatusAdmin(admin.ModelAdmin):
    list_display= ('id', 'status',)

    
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display= ('client','support_contact','event_status')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'client':
            kwargs['limit_choices_to'] ={'sales_contact_id': request.user.id}  
            
        if db_field.name == 'event_status':
            contract_ids = Contract.objects.all().filter(sales_contact_id = request.user.id)
            ids = []
            for id in list(contract_ids):
                ids.append(id.id)
            q_objects = Q(id__in=[])
            for item in ids:
                q_objects.add(Q(pk=item), Q.OR)
                
            kwargs['limit_choices_to']=q_objects  
        return super(EventAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        