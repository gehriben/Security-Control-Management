from django.db import models

class Keyword(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name    

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField('description', blank=True, null=True)
    keywords = models.ManyToManyField(Keyword, blank=True)

    def __str__(self):
        return self.name
