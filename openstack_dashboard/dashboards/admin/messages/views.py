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

from openstack_dashboard.api.telemetry import HostMessages as host

from openstack_dashboard.dashboards.admin.messages import forms as \
    messages_forms
from openstack_dashboard.dashboards.admin.messages import tabs as \
    messages_tabs


class IndexView(tabs.TabbedTableView):
    tab_group_class = messages_tabs.MessagesOverviewTabs
    template_name = 'admin/messages/index.html'


class MessageUserView(forms.ModalFormView):
    form_class = messages_forms.MessageUserForm
    template_name = 'admin/messages/message_user.html'
    success_url = reverse_lazy("horizon:admin:messages:index")

    @memoized.memoized_method
    def get_object(self):
        try:
            return api.keystone.user_get(self.request, self.kwargs['id'],
                admin=True)
        except Exception:
            redirect = reverse("horizon:admin:users:index")
            exceptions.handle(self.request,
                              _('Unable to send message for the user.'),
                              redirect=redirect)

    def get_context_data(self, **kwargs):
        context = super(MessageUserView, self).get_context_data(**kwargs)
        context['user'] = self.get_object()
        return context

    def get_initial(self):
        user = self.get_object()
        domain_id = getattr(user, "domain_id", None)
        domain_name = ''
        # Retrieve the domain name where the project belong
        if api.keystone.VERSIONS.active >= 3:
            try:
                domain = api.keystone.domain_get(self.request,
                                                    domain_id)
                domain_name = domain.name
            except Exception:
                exceptions.handle(self.request,
                    _('Unable to retrieve project domain.'))
        return {'domain_id': domain_id,
                'domain_name': domain_name,
                'id': user.id,
                'name': user.name,
                'project': user.project_id,
                'email': getattr(user, 'email', None)}


class MessageProjectView(forms.ModalFormView):
    form_class = messages_forms.MessageUserForm
    template_name = 'admin/messages/message_project.html'
    success_url = reverse_lazy("horizon:admin:messages:index")
    
    @memoized.memoized_method
    def get_object(self):
        try:
            return api.keystone.tenant_get(self.request, self.kwargs['id'],
                admin=True)
        except Exception:
            redirect = reverse("horizon:admin:users:index")
            exceptions.handle(self.request,
                              _('Unable to send message for the project.'),
                              redirect=redirect)

    def get_context_data(self, **kwargs):
        context = super(MessageProjectView, self).get_context_data(**kwargs)
        context['project'] = self.get_object()
        return context

    def get_initial(self):
        project = self.get_object()
        domain_id = getattr(project, "domain_id", None)
        domain_name = ''
        # Retrieve the domain name where the project belong
        if api.keystone.VERSIONS.active >= 3:
            try:
                domain = api.keystone.domain_get(self.request,
                                                    domain_id)
                domain_name = domain.name
            except Exception:
                exceptions.handle(self.request,
                    _('Unable to retrieve project domain.'))
        return {'domain_id': domain_id,
                'domain_name': domain_name,
                'id': project.id,
                'name': project.name}


class MessageHostView(forms.ModalFormView):
    form_class = messages_forms.MessageUserForm
    template_name = 'admin/messages/message_host.html'
    success_url = reverse_lazy("horizon:admin:messages:index")
    
    def get_context_data(self, **kwargs):
        context = super(MessageHostView, self).get_context_data(**kwargs)
        context["id"] = self.kwargs['id']
        return context
    
    def get_object(self):
        id = self.kwargs['id']
        return id
    
    def get_initial(self):
        id = self.get_object()
        return {'id': id}