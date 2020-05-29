from django.db import models
from django.contrib.postgres.fields import ArrayField
from vendor.models import Vendor

# Create your models here.
class Menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    price = models.IntegerField()
    quantity = models.IntegerField()
    date_time_created = models.DateTimeField(auto_now_add=True)
    vendor_id = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    is_recurring = models.BooleanField(default=False)
    frequency_of_reoccurence = ArrayField(
        models.CharField(max_length=10, blank=True),
        size=7,
        blank=True, 
        null=True,
        default=list)
