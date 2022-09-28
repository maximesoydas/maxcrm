from .models import Client, Contract, Event, User
from rest_framework import serializers



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'     

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        
        
class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'
        
class ContractStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'     
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'