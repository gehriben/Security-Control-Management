from django.db import models
from assets.models import Asset
from controls.models import Control

class ConstraintType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Create your models here.
class Constraint(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField('description')
    constraint_type = models.ForeignKey(ConstraintType, on_delete=models.CASCADE)
    values = models.JSONField()

    def __str__(self):
        return self.name

class ConstraintAssociation(models.Model):
    name = models.CharField(max_length=200, default="ConstraintAssociationObject")
    constraint = models.ForeignKey(Constraint, on_delete=models.CASCADE)
    selected_value = models.JSONField()
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, blank=True, null=True)
    control = models.ForeignKey(Control, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name