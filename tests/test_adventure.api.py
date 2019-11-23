import pytest
from adventure.api import initialize
from rest_framework.test import force_authenticate

pytestmark = pytest.mark.django_db

def test_initialize(client):
    pass
    #assert response.status_code == 200
