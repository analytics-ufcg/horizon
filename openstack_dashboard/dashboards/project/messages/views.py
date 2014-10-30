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
        m = MessageManager()
        message_id = self.kwargs['message_id']
        context = super(DetailView, self).get_context_data(**kwargs)
        context["message"] = self.get_data()
        context["url1"] = m.get_url(message_id)
        return context

    def get_data(self):
        try:
            message_id = self.kwargs['message_id']
            message_obj = MessageManager()
            message_obj.change_status(message_id, 'T')
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

class SnapshotView(TemplateView):
    template_name = 'project/messages/snapshot.html'
    redirect_url = 'horizon:project:messages:index'

    def get_context_data(self, **kwargs):
        context = super(SnapshotView, self).get_context_data(**kwargs)
        context["is_action_enable"] = self.get_data() 
        return context

    def get_data(self):
        try:
            message_id = self.kwargs['message_id']
            instance_id = self.kwargs['instance_id']

            message_manager = MessageManager()
            if (message_manager.is_action_enable(message_id) == 'T'):
                message_manager.execute_snapshot_action(str(instance_id))
                message_manager.disable_action(message_id)
                return True
            else:
                return False
        except Exception:
            redirect = reverse(self.redirect_url)
            exceptions.handle(self.request,
                              _('Unable to execute snapshot action for '
                                'instance "%s".') % instance_id,
                                redirect=redirect)
            # Not all exception types handled above will result in a redirect.
            # Need to raise here just in case.
            raise exceptions.Http302(redirect)
        return message_id

class SuspendView(TemplateView):
    template_name = 'project/messages/suspend.html'
    redirect_url = 'horizon:project:messages:index'

    def get_context_data(self, **kwargs):
        context = super(SuspendView, self).get_context_data(**kwargs)
        context["message_id"] = self.get_data()
        return context

    def get_data(self):
        try:
            message_id = self.kwargs['message_id']
            instance_id = self.kwargs['instance_id']
            
            message_manager = MessageManager()
            message_manager.execute_suspend_action(str(instance_id))
            #delete message after action

        except Exception:
            redirect = reverse(self.redirect_url)
            exceptions.handle(self.request,
                              _('Unable to execute suspend action for '
                                'instance "%s".') % instance_id,
                                redirect=redirect)
            # Not all exception types handled above will result in a redirect.
            # Need to raise here just in case.
            raise exceptions.Http302(redirect)
        return message_id

