from django.db import models
from order.models import Order
from message_status.models import MessageStatus

# Create your models here.
class Notification(models.Model):
    subjectUser = models.EmailField(max_length=100)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
    date_time_created = models.DateTimeField(auto_now_add=True)
    message_status = models.ForeignKey(MessageStatus, on_delete=models.CASCADE)