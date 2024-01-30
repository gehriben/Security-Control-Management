from django.db import models

from tags.models import Tag
from properties.models import Property
from controls.models import Control

# Create your models here.
class Assettype(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Asset(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField('description')
    assettype = models.ForeignKey(Assettype, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    properties = models.ManyToManyField(Property, blank=True)

    def __str__(self):
        return self.name

class AssetControlMatch(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    control = models.ForeignKey(Control, on_delete=models.CASCADE)

