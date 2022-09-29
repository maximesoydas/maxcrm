import json
from xmlrpc.client import ResponseError

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from epic_events.models import Client, Contract, ContractStatus, Event, User
from epic_events.serializers import (ClientSerializer, ContractSerializer,
                                     ContractStatusSerializer, EventSerializer)
from rest_framework.test import force_authenticate
from django.contrib.auth.models import Group


class RegistrationTestCase(APITestCase):

    def test_superuser_registration(self):
        data = {
            "username": "testadmin",
            "password": "epic_events10",
        }
        user = User.objects.create_superuser(data)
        self.client.force_authenticate(user)
        response = self.client.get("/users/")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sales_registration(self):
        data = {
            "username": "testsales",
            "password": "epic_events10",
            "groups": 'sales',
        }
        user = User.objects.create_user(data)
        self.client.force_authenticate(user)
        response = self.client.get("/users/")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_support_registration(self):
        data = {
            "username": "testsupport",
            "password": "epic_events10",
            "groups": 'support',
        }
        user = User.objects.create_user(data)
        self.client.force_authenticate(user)
        response = self.client.get("/users/")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ClientViewSetTestCase(APITestCase):

    url = "/clients/"

    def setUp(self) -> None:
        data = {
            "username": "test",
            "password": "epic_events10",
        }
        user = User.objects.create_user(data)
        self.client.force_authenticate(user)
        self.token = Token.objects.create(user=user)
        self.api_authentication()
        # Group setup
        sales_group = "sales"
        support_group = 'support'
        self.group = Group(name=sales_group)
        self.group.save()
        self.group.user_set.add(user)

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_client_list_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_create_authenticated(self):
        data = {
            "first_name": "Johnny",
            "last_name": "Customer",
            "email": "johnny@customer.fr",
            "phone": "0784578542",
            "mobile": "074587562",
            "company_name": "johnny co"
        }
        response = self.client.post(self.url, data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
