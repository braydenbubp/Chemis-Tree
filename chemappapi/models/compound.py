from django.db import models
from .user import User
from .element import Element

class Compound(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="compounds")
    common_name = models.CharField(max_length=255)
    formula = models.CharField(max_length=255)
    smiles = models.TextField()
    molecular_weight = models.FloatField(null=True, blank=True)
    chemspider_id = models.IntegerField(unique=True)
    two_d_model = models.CharField(max_length=200)
    elements = models.ManyToManyField(Element, through='CompoundElement', related_name="compounds")

    @property
    def user_id(self):
      return self.user.id
