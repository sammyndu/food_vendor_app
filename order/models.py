from django.db import models
from django.contrib.postgres.fields import ArrayField
from customer.models import Customer
from vendor.models import Vendor
from order_status.models import OrderStatus

# Create your models here.
class Order(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vendor_id = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    items_ordered = ArrayField(
        models.IntegerField(null=True, blank=True),
        size=5,
        default=list)
    amount_due = models.IntegerField()
    amount_paid = models.IntegerField()
    amount_outsanding = models.IntegerField()
    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    date_and_time_of_order = models.DateTimeField(auto_now_add=True)
