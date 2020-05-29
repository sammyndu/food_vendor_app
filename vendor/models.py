from django.db import models

# Create your models here.
class Vendor(models.Model):
    business_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=14)
    date_time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name + " " + self.email