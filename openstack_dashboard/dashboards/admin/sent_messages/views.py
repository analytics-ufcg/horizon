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

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import tables
from horizon import tabs

from messages.message_selection import MessageManager

from openstack_dashboard.api.telemetry \
    import SentMessages as sent_messages

from openstack_dashboard.dashboards.admin.sent_messages \
    import tables as sent_tables
from openstack_dashboard.dashboards.admin.sent_messages \
    import tabs as sent_tabs


class IndexView(tables.DataTableView):
    table_class = sent_tables.SentTable
    template_name = 'admin/sent_messages/index.html'

    def get_data(self):
        sent_data = []
        message_manager = MessageManager()

        for message_data in message_manager.return_all_messages():
            message_id =  message_data['id']
            subject = message_data['subject']
            sent_to = message_data['type']
            read = str(message_data['read']) + '/' + str(message_data['total'])

            sent_data.append(sent_messages(message_id, subject, sent_to, read))

        return sent_data


class DetailView(tabs.TabView):
    tab_group_class = sent_tabs.MessageDetailTabs
    template_name = 'admin/sent_messages/detail.html'
    failure_url = reverse_lazy('horizon:admin:sent_messages:index')

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context["message"] = self.get_data()
        return context

    def get_data(self):
        try:
            message_id = self.kwargs['message_id']
            message_obj = MessageManager()
            message = message_obj.get_message_info(message_id)

        except Exception:
            redirect = reverse(self.redirect_url)
            exceptions.handle(self.request,
                              _('Unable to retrieve details for '
                                'message "%s".') % message_id,
                                redirect=redirect)
            # Not all exception types handled above will result in a redirect.
            # Need to raise here just in case.
            raise exceptions.Http302(redirect)
        return message

    def get_tabs(self, request, *args, **kwargs):
        message = self.get_data()
        return self.tab_group_class(request, message=message, **kwargs)
