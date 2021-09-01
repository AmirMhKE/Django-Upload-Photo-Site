from django.db import models
from django_jalali.db import models as jmodels


class TimeStamp(models.Model):
    """
    Created Time and Updated Time for your 
    models with inheritingfrom this class.
    """
    created = jmodels.jDateTimeField(auto_now_add=True)
    updated = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        abstract = True
        