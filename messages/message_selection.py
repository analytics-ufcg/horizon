# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2014 UFCG/Analytics.
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

from messages.models import Message, MessageId, MessageRelation
from openstack_dashboard.api.telemetry_api.telemetry_data import  DataHandler
from openstack_dashboard.api.telemetry_api.openstack.nova_client import  NovaClient
from openstack_dashboard.api.telemetry_api.openstack.keystone_client import KeystoneClient
import datetime, ConfigParser


class MessageManager:
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read('openstack_dashboard/api/telemetry_api/environment.conf')
        self.__nova_client = NovaClient(config)
        self.__keystone_client = KeystoneClient(config)
        self.__projects = self.__keystone_client.get_tenants()
        
    def get_message_by_recipient(self, recipient):
        return Message.objects.filter(recipient=recipient)

    def send_message(self, subject, message, user_id, sender='admin'):
        m = Message(sender=sender, recipient=user_id,
                    subject=subject, timestamp=datetime.datetime.now(),
                    message=message, read='F')
        m.save()
        return m

    def send_message_user(self, subject, message, user_id, sender='admin'):
        ref = self.message_id('user')
        m = self.send_message(subject, message, user_id)
        self.message_relation(ref.id, m.id)
        

    def message_id(self, type):
        m = MessageId(type = type)
        m.save()
        return m

    def message_relation(self, message, message_ref):
        m = MessageRelation(id_message = message_ref, message = message)
        m.save()

    def send_message_project(self, subject, message, tenant_id, sender='admin'):
        ref = self.message_id('project')
        users = self.__keystone_client.list_project_users(tenant_id)
        for user in users:
            m = self.send_message(subject, message, user)
            self.message_relation(ref.id, m.id)
        print 'done'

    def send_message_host(self, subject, message, host_name, sender='admin'):
        ref = self.message_id('host')
        servers = self.__nova_client.get_servers_by_host(host_name)
        users_id = self.__nova_client.get_users_by_host(servers)
        users_list = list(set(users_id))
        for user in users_list:
            m = self.send_message(subject, message, user)
            self.message_relation(ref.id, m.id)
        return True

    def get_message_by_id(self, id):
        return Message.objects.filter(id=id)[0]

    def get_message_read_by_id(self, id):
        return Message.objects.filter(recipient=id, read="F")

    def delete_message(self, id):
        message = Message.objects.filter(id=id)[0]
        message.delete()



    def change_status(self, id, status):
        m = Message.objects.filter(id=id)[0]
        m.read = status
        m.save()
