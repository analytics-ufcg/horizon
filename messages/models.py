# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2014, UFCG/Analytics
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

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

class MessageId(models.Model):
    type = models.CharField(max_length=10)
    
class MessageRelation(models.Model):
    id_message = models.IntegerField()
    message = models.IntegerField()

class TemplateMessage(models.Model):
    id_message = models.IntegerField()
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=50000)
    actions = models.CharField(max_length=100)


#For user.py file 
def user_messages(self):
    return Message.objects.filter(recipient=self.id, read="F")

