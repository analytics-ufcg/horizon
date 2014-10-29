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

from django.utils.translation import ugettext_lazy as _
from messages.message_selection import MessageManager
from horizon import tables


class DetailMessageAction(tables.LinkAction):
    name = "detail_message"
    verbose_name = _("Message Detail")
    url = "horizon:admin:sent_messages:detail"
    classes = ('btn-edit')

class DeleteMessageAction(tables.DeleteAction):
    data_type_singular = _("Message")
    data_type_plural = _("Messages")

    def delete(self, request, obj_id):
        m = MessageManager()
        m.delete_admin_message(obj_id)



class SentTable(tables.DataTable):
    message_id = tables.Column("message_id",
                        verbose_name=_("ID"))
    subject = tables.Column("subject",
                        verbose_name=_("Subject"))
    sent_to = tables.Column("sent_to",
                        verbose_name=_("Sent To"))
    read = tables.Column('read',
                        verbose_name=_("Read/Total"))

    def get_object_id(self, obj):
        return "%s" % (obj.message_id)

    class Meta:
        name = "sent_table"
        verbose_name = _("Messages")
        row_actions = (DetailMessageAction,)
        table_actions = (DeleteMessageAction,)
