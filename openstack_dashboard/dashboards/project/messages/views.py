# vim: tabstop=4 shiftwidth=4 softtabstop=4

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

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView  # noqa

from horizon import exceptions
from horizon import tables

from messages.message_selection import MessageManager

from openstack_dashboard.api.telemetry \
    import UserMessages as user_messages
from openstack_dashboard.dashboards.project.messages \
    import tables as messages_tables


class IndexView(tables.DataTableView):
    table_class = messages_tables.MessagesTable
    template_name = 'project/messages/index.html'

    def get_data(self):
        messages_table = []
        message_obj = MessageManager()
        messages_list \
            = message_obj.get_message_by_recipient(self.request.user.id)

        for messages in messages_list:
            message = user_messages(messages.id, messages.sender,
                                    messages.subject, messages.timestamp,
                                    messages.message, messages.read)
            messages_table.append(message)

        return messages_table


class DetailView(TemplateView):
    template_name = 'project/messages/detail.html'
    redirect_url = 'horizon:project:messages:index'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context["message"] = self.get_data()
        return context

    def get_data(self):
        try:
            message_id = self.kwargs['message_id']
            message_obj = MessageManager()
            message = message_obj.get_message_by_id(message_id)
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
