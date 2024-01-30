from django.db import models
from tags.models import Tag

# Create your models here.
class Control(models.Model):
    cn = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    description = models.TextField('description')
    parent_control = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name