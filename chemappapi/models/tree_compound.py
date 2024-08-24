from django.db import models
from .compound import Compound
from .tree import Tree

class TreeCompound(models.Model):
    compound = models.ForeignKey(Compound, on_delete=models.CASCADE, related_name='trees')
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
