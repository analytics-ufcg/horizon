# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2014 UFCG.
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

from messages.models import Message

import datetime


class MessageManager:
    def get_message_by_recipient(self, recipient):
        return Message.objects.filter(recipient=recipient)

    def send_message(self, sender, recipient, subject, message):
        m = Message(sender=sender, recipient=recipient,
                    subject=subject, timestamp=datetime.datetime.now(),
                    message=message, read='F')
        m.save()

    def get_message_by_id(self, id):
        return Message.objects.filter(id=id)[0]

    def get_message_read_by_id(self, id):
        return Message.objects.filter(recipient=id, read="F")

    def change_status(self, id, status):
        m = Message.objects.filter(id=id)[0]
        m.read = status
        m.save()
