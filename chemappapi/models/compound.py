from django.db import models
from .user import User
from .element import Element

class Compound(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="compounds")
    iupac_name = models.CharField(max_length=255)
    molecular_formula = models.CharField(max_length=255)
    molecular_weight = models.FloatField(null=True, blank=True)
    cid = models.IntegerField(unique=True)
    bonds = models.JSONField(default=list)
    synonyms = models.JSONField(default=list)
    elements = models.ManyToManyField(Element, through='CompoundElement', related_name="compounds")
    model_2d = models.ImageField(upload_to='compound_models/', null=True, blank=True)

    @property
    def user_id(self):
      return self.user.id
