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
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import tabs
from horizon.utils import memoized

from openstack_dashboard import api

from openstack_dashboard.dashboards.admin.messages import forms as \
    messages_forms
from openstack_dashboard.dashboards.admin.messages import tabs as \
    messages_tabs


class IndexView(tabs.TabbedTableView):
    tab_group_class = messages_tabs.MessagesOverviewTabs
    template_name = 'admin/messages/index.html'


class MessageView(forms.ModalFormView):
    form_class = messages_forms.MessageUserForm
    template_name = 'admin/messages/message.html'
    success_url = reverse_lazy("horizon:admin:messages:index")

'''
    @memoized.memoized_method
    def get_object(self):
        try:
            return api.keystone.user_get(self.request, self.kwargs['id'],
                admin=True)
        except Exception:
            redirect = reverse("horizon:admin:messages:index")
            exceptions.handle(self.request,
                              _('Unable to send message.'),
                              redirect=redirect)

    def get_context_data(self, **kwargs):
        context = super(MessageView, self).get_context_data(**kwargs)
        context['user'] = self.get_object()
        return context

    def get_initial(self):
        user = self.get_object()
        return {'name': user.name,
                'email': getattr(user, 'email', None),
                'id': user.id}
'''
