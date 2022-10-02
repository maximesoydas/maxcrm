import re
from django.shortcuts import render
from django.views import View
# Create your views here.
from .models import Client, Contract, ContractStatus, Event, User
from rest_framework import viewsets
from rest_framework import permissions, filters
from .serializers import ClientSerializer, ContractSerializer, EventSerializer, UserSerializer, ContractStatusSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.forms.models import model_to_dict
from django_filters.rest_framework import DjangoFilterBackend

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends=[DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id']
    search_fields = ['id']
    ordering_fields = ['id']
    def list(self, request):
        if request.user.is_superuser:
            queryset = User.objects.all()
            serializer = UserSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data="Only Management/superusers can view users")

    def create(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().create(request, *args, **kwargs)
        else:
            data = "Only Management/superusers can register a new client"
            return Response(data)
        
        
    def update(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().update(request, *args, **kwargs)
        else:
            data = "//!\ Cannot Update //!\ (only a superuser(manager) can update users)"
            return Response(data)
        
    def destroy(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().destroy(request, *args, **kwargs)
        else:
            return Response(data="//!\ Cannot Delete //!\ (only a superuser(manager) can delete clients)")
            
class ClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Client.objects.all().order_by('-date_create')
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends=[DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['first_name','last_name','email']
    search_fields = ['first_name','last_name','email']
    ordering_fields = ['first_name','last_name','email']
    
    
    def list(self, request):
        if request.user.is_superuser:
            queryset = Client.objects.all()
            serializer = ClientSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.user.groups.filter(name='sales'):
            queryset = Client.objects.all().filter(sales_contact=self.request.user.id)
            serializer = ClientSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.user.groups.filter(name='support'):
            # return only clients related to the event 'supported' by the user
            queryset = Client.objects.all().filter(event__support_contact=self.request.user.id)
            serializer = ClientSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            data = "Only a sales person can read a new client"
            return Response(data)


    def create(self, request, *args, **kwargs):
        if request.user.groups.filter(name='sales'):
            request.data['sales_contact'] = request.user.id
            return super().create(request, *args, **kwargs)
        else:
            data = "Only a sales person can register a new client"
            return Response(data)

    def update(self, request, *args, **kwargs):
        if request.user.groups.filter(name='sales'):
            try:
                print(kwargs['pk'])
                field_name = 'sales_contact'
                obj = Client.objects.all().filter(id=kwargs['pk']).first()
                sales_contact = getattr(obj, field_name)
                if sales_contact == self.request.user:
                    request.data['sales_contact'] = request.user.id
                    return super().update(request, *args, **kwargs)
                # else
            except AttributeError:
                data= f"//!\ Cannot Update //!\ (the client with the ID number {kwargs['pk']} does not exist)"
                return Response(data)
                
        elif request.user.is_superuser:
            return super().update(request, *args, **kwargs)
        else:
            data = "//!\ Cannot Update //!\ (only a sales person or a superuser(admin) can update clients)"
            return Response(data)
        
    def destroy(self, request, *args, **kwargs):
        if request.user.groups.filter(name='sales'):
            try:  
                print(kwargs['pk'])
                field_name = 'sales_contact'
                obj = Client.objects.all().filter(id=kwargs['pk']).first()
                sales_contact = getattr(obj, field_name)
                if sales_contact == self.request.user:
                    return super().destroy(request, *args, **kwargs)
            except AttributeError:
                data= f"//!\ Cannot Delete //!\ (the client with the ID number {kwargs['pk']} does not exist)"
                return Response(data)
        else:
            return Response(data="//!\ Cannot Delete //!\ (only a sales person or a superuser(admin) can delete clients)")
            
          
class ContractViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Contract.objects.all().order_by('-date_create')
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends=[DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['client__first_name','client__last_name','client__email','amount','date_create']
    search_fields = ['client__first_name','client__last_name','client__email','amount','date_create']
    ordering_fields = ['client__first_name','client__last_name','client__email','amount','date_create']

   
   
    def list(self, request):
        if request.user.is_superuser:
            queryset = Contract.objects.all()
            serializer = ContractSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.user.groups.filter(name='sales'):
            queryset = Contract.objects.all().filter(sales_contact=self.request.user.id)
            serializer = ContractSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.user.groups.filter(name='support'):
            data = "Only salesman or superuser can see contracts"
            return Response(data)
        else:
            data = "Only contracts related to the user can be shown"
            return Response(data)

    def create(self, request, *args, **kwargs):
        
        if request.user.groups.filter(name='sales'):
            print(request.data)
            request.data['sales_contact'] = request.user.id
            # check if the entered client has the request.user as a sales_Contact
            user_clients = Client.objects.all().filter(sales_contact=self.request.user.id)
            for client in user_clients:
                if client.sales_contact.id == request.data['sales_contact']:                    
                    # when u create a contract u also need to create a contractstatus with the same ID
                    # Get the id of the newly created contract
                    serializer = self.get_serializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    self.perform_create(serializer)
                    # create a contractstatus with the id of the newly created contract
                    ContractStatus.objects.create(id=serializer.instance.pk, status=request.data['status'])
                    return Response({'status': 'success', 'pk': serializer.instance.pk})

                else:
                    data = "Only clients of current xzz/sales_contact can be attributed to a contract"
                    return Response(data)
        else:
            data = "Only a sales person can register a new contract"
            return Response(data)

    def update(self, request, *args, **kwargs):
        if request.user.groups.filter(name='sales'):
            try:
                queryset = Contract.objects.all().filter(id=kwargs['pk']).first()
                if queryset.sales_contact.id == self.request.user.id:
                    contractstatus = ContractStatus.objects.all().filter(id=kwargs['pk']).first()
                    contractstatus.status = request.data['status']
                    contractstatus.save()
                    return super().update(request, *args, **kwargs)

            except AttributeError:
                data= f"//!\ Cannot Update //!\ (the contract with the ID number {kwargs['pk']} does not exist)"
                return Response(data)
                
        elif request.user.is_superuser:
            return super().update(request, *args, **kwargs)
        else:
            data = "//!\ Cannot Update //!\ (only a sales person or a superuser(admin) can update contracts)"
            return Response(data)
        
    def destroy(self, request, *args, **kwargs):
        if request.user.groups.filter(name='sales'):
            try:  
                queryset = Contract.objects.all().filter(id=kwargs['pk']).first()
                if queryset.sales_contact.id == self.request.user.id:
                    # contractstatus = ContractStatus.objects.all().filter(id=kwargs['pk']).first()
                    # contractstatus.delete()
                    return super().destroy(request, *args, **kwargs)
                else:
                    return Response(data="//!\ Cannot Delete //!\ (only a sales person can delete contracts)")
                    
            except AttributeError:
                data= f"//!\ Cannot Delete //!\ (the client with the ID number {kwargs['pk']} does not exist)"
                return Response(data)
        else:
            return Response(data="//!\ Cannot Delete //!\ (only a sales person or a superuser(admin) can delete contracts)")



class ContractStatusViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Event.objects.all().order_by('-date_create')
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        if request.user.is_superuser:
            queryset = ContractStatus.objects.all()
            serializer = ContractStatusSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.user.groups.filter(name='sales'):
            user_contracts = Contract.objects.all().filter(sales_contact=self.request.user.id)
            user_contracts_list = []
            for user_contract in user_contracts:
                # user_contracts_list.append(user_contract.id)
                queryset= ContractStatus.objects.all().filter(id=user_contract.id).first()
                if queryset is None:
                    pass
                else:
                    # serializer = ContractStatusSerializer(queryset)
                    # print(serializer.data)
                    pk = getattr(queryset, 'id')
                    status = getattr(queryset, 'status')
                    contractstatus = {'id': pk , 'status': status}
                    user_contracts_list.append(contractstatus)
            
            data = user_contracts_list
            # data = 'ds'
            return Response(data)

        if request.user.groups.filter(name='support'):
            # return only clients related to the event 'supported' by the user
            data = 'Only salesperson can see their contractstatus'
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)


class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Event.objects.all().order_by('-date_create')
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends=[DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['client__first_name','client__last_name','client__email', 'event_date']
    search_fields = ['client__first_name','client__last_name','client__email', 'event_date']
    ordering_fields = ['client__first_name','client__last_name','client__email', 'event_date']

    
    def list(self, request):
        if request.user.is_superuser:
            queryset = Event.objects.all()
            serializer = EventSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.user.groups.filter(name='sales'):
            queryset = Event.objects.all()
            serializer = EventSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.user.groups.filter(name='support'):
            # return only clients related to the event 'supported' by the user
            queryset = Event.objects.all().filter(support_contact=self.request.user.id)
            serializer = EventSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        
        if request.user.groups.filter(name='sales'):
            # try:
            event_status = request.data['event_status']
            contract = Contract.objects.all().filter(id=int(event_status)).first()
            client = Client.objects.all().filter(id=request.data['client']).first()
            # event_status must redirect to a contract related to the user
            contract_sales_contact = getattr(contract, 'sales_contact')
            client_sales_contact = getattr(client, 'sales_contact')
            if contract_sales_contact == self.request.user:
                # check if the entered client has the request.user as a sales_Contact
                if client_sales_contact == self.request.user:
                    # request.data['support_contact'] = 'null'
                    return super().create(request, *args, **kwargs)
                else:
                    data = "The client is not related to the current user/salesperson"
            else:
                data = "The contract is not related to the current user/salesperson"
            # except AttributeError:
            #     data= f"//!\ Cannot Create //!\ (the ContractStatus with the ID number {event_status} does not exist)"
            #     return Response(data)
        else:
            data = "Only a sales person can register a new event"
            return Response(data)
        

    def update(self, request, *args, **kwargs):
        if request.user.groups.filter(name='sales'):
            try:
                print(kwargs['pk'])
                field_name = 'client'
                obj = Event.objects.all().filter(id=kwargs['pk']).first()
                client = getattr(obj, field_name)
                client_obj = Client.objects.all().filter(id=client.id).first()
                print(client_obj.sales_contact)
                print("TESTESTES")
                if client_obj.sales_contact == self.request.user:
                    # request.data['sales_contact'] = request.user.id
                    return super().update(request, *args, **kwargs)
                # else error
            except AttributeError:
                data= f"//!\ Cannot Update //!\ (the client with the ID number {kwargs['pk']} does not exist)"
                return Response(data)
                
        elif request.user.is_superuser:
            return super().update(request, *args, **kwargs)
        else:
            data = "//!\ Cannot Update //!\ (only a sales person or a superuser(admin) can update clients)"
            return Response(data)
        
    def destroy(self, request, *args, **kwargs):
        if request.user.groups.filter(name='sales'):
            try:  
                print(kwargs['pk'])
                field_name = 'client'
                obj = Event.objects.all().filter(id=kwargs['pk']).first()
                client = getattr(obj, field_name)
                if client.sales_contact == self.request.user:
                    return super().destroy(request, *args, **kwargs)
            except AttributeError:
                data= f"//!\ Cannot Delete //!\ (the event with the ID number {kwargs['pk']} does not exist)"
                return Response(data)
        else:
            return Response(data="//!\ Cannot Delete //!\ (only a sales person or a superuser(admin) can delete events)")
              

class Index(View):
    def get(self, request):
        return render(request, 'epic_events/index.html')