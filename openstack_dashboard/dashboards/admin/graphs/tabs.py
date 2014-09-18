# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from django.utils.translation import ugettext_lazy as _

from horizon  import tabs
from openstack_dashboard.api.telemetry_api.telemetry_data import DataHandler
import json
import requests
import ast, ConfigParser

data_handler = DataHandler()
HOSTS = ast.literal_eval(data_handler.get_config().get('Openstack', 'computenodes'))

class HostsTab(tabs.Tab):
    name = _("Hosts")
    slug = "hosts"
    template_name = ("admin/graphs/hosts.html")

    def get_context_data(self, request, *args, **kwargs):
        context_temp = {'name':'hosts','children':[]}
        for h in HOSTS:
            host = {'ip':h}
            context_temp['children'].append(host)
        host_list = context_temp['children']
        context = {'hosts_list': host_list}
        return context


class AggregatesTab(tabs.Tab):
    name = _("Aggregates")
    slug = "aggregates"
    template_name = ("admin/graphs/aggregates.html")

    def get_context_data(self, request):
        agg_list = []
        agg_list = data_handler.host_aggregates('admin')
        context = {'agg_list': agg_list}
        return context


class ProjectsTab(tabs.Tab):
    name = ("Projects")
    slug = "projects_meter"
    template_name = ("admin/graphs/projects.html")

    def get_context_data(self, request):
        projs = data_handler.projects_with_instances_and_cpu_util()['children']
        projects = {}
        for p in projs:
            if len(p['children']) > 0:
                projects[p['name']] = p['children']

        context = {'projects': projects,
                   'projects_json': json.dumps(projects)}

        return context


class GraphsTabs(tabs.TabGroup):
    slug = "graphs_overview"
    tabs = (AggregatesTab, HostsTab, ProjectsTab, )
    #tabs = (HostsTab,AggregatesTab,)
    sticky = True
