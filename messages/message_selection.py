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

    def send_message_project(self, subject, message, tenant_id, sender='admin'):
        users = self.__keystone_client.list_project_users(tenant_id)
        for user in users:
            self.send_message(sender, user, subject, message)

    def send_message_host(self, subject, message, host_name, sender='admin'):
        servers = self.__nova_client.get_servers_by_host(host_name, ['admin', 'demo'])
        users_id = self.__nova_client.get_users_by_host(servers)
        users_list = list(set(users_id))
        for user in users_list:
            self.send_message(sender, user, subject, message)
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
