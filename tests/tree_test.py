from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from chemappapi.models import Compound, User, Tree
from chemappapi.views.tree import TreeSerializer
from chemappapi.views.compound import CompoundSerializer
