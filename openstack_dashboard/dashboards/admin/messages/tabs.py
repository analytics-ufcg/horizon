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

from horizon import exceptions

from openstack_dashboard.dashboards.admin.messages import tables

from openstack_dashboard import api

from openstack_dashboard.api.telemetry_api.openstack.keystone_client \
    import KeystoneClient
from openstack_dashboard.api.telemetry_api.openstack.nova_client \
    import NovaClient

from horizon import tabs

import ConfigParser


class UsersTab(tabs.TableTab):
    table_classes = (tables.UsersTable,)
    name = _("Users")
    slug = "users_tab"
    template_name = ("horizon/common/_detail_table.html")

    def get_users_data(self):
        users_data = []
#        domain_context = self.request.session.get('domain_context', None)

        try:
             config = ConfigParser.ConfigParser()
             config.read('openstack_dashboard/api/telemetry_api/environment.conf')
             keystone_client = KeystoneClient(config)

             for user in keystone_client.list_users():
                 users_obj = api.telemetry.MessagesUser(user.username, user.email, user.id)
#            users_data = api.keystone.user_list(self.request,
#                                           domain=domain_context)
                 users_data.append(users_obj)
        except Exception:
            exceptions.handle(self.request,
                              _('Unable to retrieve user list.'))

        return users_data


class ProjectsTab(tabs.TableTab):
    table_classes = (tables.ProjectsTable,)
    name = _("Projects")
    slug = "projects_tab"
    template_name = ("horizon/common/_detail_table.html")

    def get_projects_data(self):
        tenants = []
        marker = self.request.GET.get(
            tables.ProjectsTable._meta.pagination_param, None)
        domain_context = self.request.session.get('domain_context', None)
        try:
            tenants, self._more = api.keystone.tenant_list(
                self.request,
                domain=domain_context,
                paginate=True,
                marker=marker)
        except Exception:
            self._more = False
            exceptions.handle(self.request,
                              _("Unable to retrieve project list."))
        return tenants

class HostsTab(tabs.TableTab):
    table_classes = (tables.HostsTable,)
    name = _("Hosts")
    slug = "hosts_tab"
    template_name = ("horizon/common/_detail_table.html")

    def get_hosts_data(self):
        hosts_data = []
        config = ConfigParser.ConfigParser()
        config.read('openstack_dashboard/api/telemetry_api/environment.conf')
        nova_client = NovaClient(config)

        for host in nova_client.list_compute_nodes():
            host_obj = api.telemetry.HostMessages(host.host_name, host.zone)
            hosts_data.append(host_obj)

        return hosts_data


class MessagesOverviewTabs(tabs.TabGroup):
    slug = "messages_overview"
    tabs = (UsersTab, ProjectsTab, HostsTab,)
    sticky = True
