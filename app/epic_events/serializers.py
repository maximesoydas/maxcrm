from .models import Client, Contract, Event
from rest_framework import serializers

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