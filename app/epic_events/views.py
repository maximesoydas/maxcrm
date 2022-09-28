from ast import Delete
from gc import DEBUG_COLLECTABLE
from django.shortcuts import render
from django.views import View
# Create your views here.
from .models import Client, Contract, ContractStatus, Event, User
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ClientSerializer, ContractSerializer, EventSerializer, UserSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
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
        
        serializer = ClientSerializer(queryset, many=True)
        return Response(serializer.data)

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
            # return only clients related to the event 'supported' by the user
            queryset = Contract.objects.all().filter(event__support_contact=self.request.user.id)
            serializer = ContractSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        serializer = ContractSerializer(queryset, many=True)
        return Response(serializer.data)

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
                obj = Contract.objects.all().filter(id=kwargs['pk']).first()
                sales_contact = getattr(obj, field_name)
                if sales_contact == self.request.user:
                    request.data['sales_contact'] = request.user.id
                    return super().update(request, *args, **kwargs)
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
              
              
class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Event.objects.all().order_by('-date_create')
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        if request.user.is_superuser:
            queryset = Event.objects.all()
            serializer = EventSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.user.groups.filter(name='sales'):
            queryset = Event.objects.all().filter(client__sales_contact=self.request.user.id)
            serializer = EventSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.user.groups.filter(name='support'):
            # return only clients related to the event 'supported' by the user
            queryset = Event.objects.all().filter(event__support_contact=self.request.user.id)
            serializer = EventSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if request.user.groups.filter(name='sales'):
            # request.data['sales_contact'] = request.user.id
            return super().create(request, *args, **kwargs)
        else:
            data = "Only a sales person can register a new client"
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
                field_name = 'sales_contact'
                obj = Event.objects.all().filter(id=kwargs['pk']).first()
                sales_contact = getattr(obj, field_name)
                if sales_contact == self.request.user:
                    return super().destroy(request, *args, **kwargs)
            except AttributeError:
                data= f"//!\ Cannot Delete //!\ (the client with the ID number {kwargs['pk']} does not exist)"
                return Response(data)
        else:
            return Response(data="//!\ Cannot Delete //!\ (only a sales person or a superuser(admin) can delete clients)")
              

class Index(View):
    def get(self, request):
        return render(request, 'epic_events/index.html')