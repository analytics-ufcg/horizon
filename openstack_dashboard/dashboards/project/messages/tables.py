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

from django import template
from django.utils.translation import ugettext_lazy as _
from messages.message_selection import MessageManager
from horizon import tables


class MessagesFilterAction(tables.FilterAction):
    def filter(self, messages_table, filter_string):
        q = filter_string.lower()

        def comp(messages_table):
            if q in messages_table.type.lower():
                return True
            return False
        return filter(comp, messages_table)


class DeleteMessagesAction(tables.DeleteAction):
    data_type_singular = _("Message")
    data_type_plural = _("Messages")

    def delete(self, request, obj_id):
        message = MessageManager()
        message.delete_message(obj_id)

class ReadMessageAction(tables.LinkAction):
    name = "read_message"
    verbose_name = _("Read Message")
    url = "horizon:project:messages:detail"
    classes = ("btn-launch", "ajax-model")


def get_senders(message):
    template_name = 'project/messages/_senders.html'
    context = {"senders": message.sender, "read": message.read}
    return template.loader.render_to_string(template_name, context)


def get_subjects(message):
    template_name = 'project/messages/_subjects.html'
    context = {"subjects": message.subject, "read": message.read}
    return template.loader.render_to_string(template_name, context)


def get_timestamps(message):
    template_name = 'project/messages/_timestamps.html'
    context = {"timestamps": message.timestamp, "read": message.read}
    return template.loader.render_to_string(template_name, context)


class MessagesTable(tables.DataTable):
    sender = tables.Column(get_senders,
                           verbose_name=_('Sender'))
    subject = tables.Column(get_subjects,
                            verbose_name=_('Subject'))
    timestamp = tables.Column(get_timestamps,
                              verbose_name=_('Date'))

    def get_object_id(self, obj):
        return "%s" % (obj.id)

    class Meta:
        name = "messages_table"
        verbose_name = _("Messages")
        row_actions = (ReadMessageAction,)
        table_actions = (MessagesFilterAction, DeleteMessagesAction)
