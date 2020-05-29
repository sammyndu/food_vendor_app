from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class MessageStatus(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = _('message status')