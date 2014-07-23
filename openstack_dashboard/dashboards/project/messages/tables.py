# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 B1 Systems GmbH
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

from django.utils.translation import ugettext_lazy as _

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
        return True


class MessagesTable(tables.DataTable):
    sender = tables.Column("sender",
                           verbose_name=_('Sender'))
    subject = tables.Column("subject",
                            link=("horizon:project:messages:detail"),
                            verbose_name=_('Subject'))
    timestamp = tables.Column("timestamp",
                              verbose_name=_('Date'))

    def get_object_id(self, obj):
        return "%s" % (obj.id)

    class Meta:
        name = "messages_table"
        verbose_name = _("Messages")
        table_actions = (MessagesFilterAction, DeleteMessagesAction)
