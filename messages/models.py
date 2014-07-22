import sys
from django.db import models

class Message(models.Model):
    sender = models.CharField(max_length=100)
    recipient = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    timestamp = models.DateTimeField('Data Published')
    message = models.TextField(max_length=50000)
    read = models.CharField(max_length=1)

    def change_status(self, status):
        if(status == 'T' or status == 'F'):
            self.read = status



# Create your models here.
