import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from epic_events.models import Client, Contract, ContractStatus, Event
from epic_events.serializers import (ClientSerializer, ContractSerializer,
                                     ContractStatusSerializer, EventSerializer)


class RegistrationTestCase(APITestCase):
    
    def test_registration(self):
        data = {"username":"testadmin", "email": "test@admin.com",
                "password1": "some_strong_psw", "password2": "some_strong_psw",}
        response = self.client.post("/api-auth/registration/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)