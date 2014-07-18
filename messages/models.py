import sys
from django.db import models

class message_module(models.Model):
    sender = models.CharField(max_length=30)
    recipient = models.CharField(max_length=30)
    subject = models.CharField(max_length=100)
    timestamp = models.DateTimeField('Data Published')
    message = models.CharField(max_length=10000)
    read = models.CharField(max_length=1)

    def change_status(self, status):
        if(status == 'T' or status == 'F'):
            self.read = status



# Create your models here.
