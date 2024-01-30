from django.db import models

class PropertyTag(models.Model):
    name = models.CharField(max_length=200)
    property_keywords = models.TextField('property_keywords')

    def __str__(self):
        return self.name

# Create your models here.
class Property(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField('description')
    parent_property = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    property_tags = models.ManyToManyField(PropertyTag, blank=True)

    def __str__(self):
        return self.name
