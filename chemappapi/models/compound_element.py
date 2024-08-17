from django.db import models
from .compound import Compound
from .element import Element

class CompoundElement(models.Model):
    compound = models.ForeignKey(Compound, on_delete=models.CASCADE)
    element = models.ForeignKey(Element, on_delete=models.CASCADE)
