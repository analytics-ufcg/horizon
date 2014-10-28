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

from messages.models import Message, MessageId, MessageRelation, TemplateMessage
from openstack_dashboard.api.telemetry_api.telemetry_data import  DataHandler
import datetime, ConfigParser


class MessageManager:
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read('openstack_dashboard/api/telemetry_api/environment.conf')
        self.__data_handler = DataHandler()
        self.__nova_client = self.__data_handler._DataHandler__nova
        self.__keystone_client = self.__data_handler._DataHandler__keystone
        self.__projects = self.__keystone_client.get_tenants()
        
    def get_message_by_recipient(self, recipient):
        return Message.objects.filter(recipient=recipient)

    def send_message(self, subject, message, user_id, sender='admin'):
        m = Message(sender=sender, recipient=user_id,
                    subject=subject, timestamp=datetime.datetime.now(),
                    message=message, read='F')
        m.save()
        return m

    def send_message_user(self, subject, message, user_id, url, sender='admin'):
        ref = self.message_id('user')
        m = self.send_message(subject, message, user_id)
        self.message_relation(ref.id, m.id, url)
        

    def message_id(self, type):
        m = MessageId(type = type)
        m.save()
        return m

    def message_relation(self, message, message_ref, url):
        m = MessageRelation(id_message = message_ref, message = message, url=url)
        m.save()

    def send_message_project(self, subject, message, tenant_id, template_id, sender='admin'):
        ref = self.message_id('project')
        servers = self.__nova_client.get_servers_by_project(tenant_id)
        
        users_id = self.__nova_client.get_instance_users_by_project(servers)
        users_list = users_id
        if template_id == 'none':
            for user in list(set(users_id.values())):
                m = self.send_message(subject, message, user)
                self.message_relation(ref.id, m.id, None)
        else:
            template = TemplateMessage.objects.filter(id_message = template_id)[0]
            action =  template.actions
            for instance in list(set(users_id.keys())):
                m = self.send_message(subject, message, users_id[instance])
                self.message_relation(ref.id, m.id, instance+'/'+action)

        return True
    def send_message_host(self, subject, message, host_name, template_id, sender='admin'):
        ref = self.message_id('host')
        servers = self.__nova_client.get_servers_by_host(host_name)
        users_id = self.__nova_client.get_instance_users_by_host(servers)
        users_list = users_id
        if template_id == 'none':
            for user in list(set(users_id.values())):
                m = self.send_message(subject, message, user)
                self.message_relation(ref.id, m.id, None)
        else:
            template = TemplateMessage.objects.filter(id_message=template_id)[0]
            action =  template.actions
            for instance in list(set(users_id.keys())):
                m = self.send_message(subject, message, users_id[instance])
                self.message_relation(ref.id, m.id, instance+'/'+action)
        return True

    def get_message_by_id(self, id):
        return Message.objects.filter(id=id)[0]

    def get_message_read_by_id(self, id):
        return Message.objects.filter(recipient=id, read="F")

    def get_url(self, id):
        return MessageRelation.objects.filter(id_message=id)[0].url

    def delete_message(self, id):
        message = Message.objects.filter(id=id)[0]
        message.delete()
        message_relation = MessageRelation.objects.filter(id_message=id)[0]
        message_relation.delete()

    def delete_admin_message(self, id):
        message = MessageId.objects.filter(id=id)[0]
        message.delete()

    def return_all_messages(self):
        
        messages_list = []
        messages = MessageId.objects.all()

        for message in messages:
            id = message.id
            relation = MessageRelation.objects.filter(message = message.id)

            if len(relation) != 0:
                id_message = relation[0].id_message
                message_table = Message.objects.filter(id=id_message) 
                subject = message_table[0].subject 
                message_type = message.type 
                total = len(MessageRelation.objects.filter(message = message.id))    
                unread = 0
                read = 0

                for id_message in relation:
                    message_table = Message.objects.filter(id=id_message.id_message)

                    if message_table[0].read == 'T':
                        read += 1;
                    else:
                        unread += 1

                message_details = {'id': id, 'subject' : subject, 'type' : message_type, 'total' : total , 'unread':unread, 'read':read }
                messages_list.append(message_details)


        return messages_list

    def get_message_info(self, message_id):
        messages = MessageId.objects.filter(id=message_id)
        relation = []

        if len(messages) > 0:
            message = messages[0]
            relation = MessageRelation.objects.filter(message = message.id)

        if len(relation)==0 or len(messages)==0:
             return False

        read= []
        unread = []

        for message in relation:
            id_message = message.id_message
            message_table = Message.objects.filter(id=id_message) 
            text = message_table[0].message

            for m in message_table:
                if m.read == 'F':
                    unread.append(self.__keystone_client.get_username(m.recipient).username)
                else:
                    read.append(self.__keystone_client.get_username(m.recipient).username)

        return {'read':read, 'unread':unread, 'text':text}


    def change_status(self, id, status):
        m = Message.objects.filter(id=id)[0]
        m.read = status
        m.save()

    def get_templates(self):
        message_templates = TemplateMessage.objects.all()
        template_data = {}
        for template in message_templates:
            template_details = {template.id: {'name': template.name, 'subject': template.subject, 'message': template.message, 'actions': template.actions}}
            template_data.update(template_details)

        return template_data

    def execute_snapshot_action(self, instance_id):
        self.__data_handler.create_snapshot(instance_id)

    def execute_suspend_action(self, instance_id):
        self.__data_handler.suspend_instance(instance_id)
