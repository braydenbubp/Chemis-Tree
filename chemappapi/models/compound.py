from django.db import models
from .user import User
from .element import Element

class Compound(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="compounds")
    iupac_name = models.CharField(max_length=255)
    molecular_formula = models.CharField(max_length=255)
    molecular_weight = models.FloatField(null=True, blank=True)
    cid = models.IntegerField(unique=True)
    bonds = models.CharField(max_length=200)
    synonyms = models.CharField(max_length=100)
    elements = models.ManyToManyField(Element, through='CompoundElement', related_name="compounds")

    @property
    def user_id(self):
      return self.user.id
