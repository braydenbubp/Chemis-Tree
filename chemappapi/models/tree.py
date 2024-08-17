from django.db import models
from .user import User

class Tree(models.Model):
    name = models.CharField(max_length=50)
    uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tree")
