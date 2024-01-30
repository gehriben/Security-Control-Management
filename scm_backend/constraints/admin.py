from django.contrib import admin
from .models import Constraint, ConstraintAssociation, ConstraintType

admin.site.register(ConstraintType)
admin.site.register(Constraint)
admin.site.register(ConstraintAssociation)
# Register your models here.
