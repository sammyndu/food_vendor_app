from django.db import models

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=14)
    date_time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + " " + self.last_name