from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from chemappapi.models import Element
from chemappapi.views.element import ElementSerializer
