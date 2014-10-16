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

from horizon import tables

from messages.message_selection import MessageManager

from openstack_dashboard.api.telemetry \
    import SentMessages as sent_messages

from openstack_dashboard.dashboards.admin.sent_messages \
    import tables as sent_tables


class IndexView(tables.DataTableView):
    table_class = sent_tables.SentTable
    template_name = 'admin/sent_messages/index.html'

    def get_data(self):
        sent_data = []
        message_manager = MessageManager()

        for message_data in message_manager.return_all_messages():
            id =  message_data['id']
            subject = message_data['subject']
            sent_to = message_data['type']
            read = str(message_data['lidas']) + '/' + str(message_data['total'])

            sent_data.append(sent_messages(id, subject, sent_to, read))

        return sent_data
