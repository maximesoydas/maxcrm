from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
import pytest
from rest_framework import status

@pytest.fixture
def api_client():
    user = User.objects.create_superuser(username='admin', email='admin@admin.com', password='admin')
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    return client

@pytest.mark.django_db
def test_read_clients(api_client):
    # Add your logic here
    url = reverse('localhost:8000/clients/')
    response = api_client.get(url)
    data = response.data

    assert response.status_code == status.HTTP_200_OK
    # your asserts