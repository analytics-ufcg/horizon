# Copyright 2014, UFCG/Analytics
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

from django import template
from django.utils.translation import ugettext_lazy as _ # noqa

from openstack_dashboard.api.telemetry_api.telemetry_data import DataHandler
import ast

from horizon import tabs
from openstack_dashboard.dashboards.admin.availability import tables

data_handler = DataHandler()
HOSTS = ast.literal_eval(data_handler.get_config().get('Openstack', 'computenodes'))

class HostTab(tabs.Tab):
    name = _("Host")
    slug = "host"
    template_name = ("admin/availability/host.html")

    def get_context_data(self, request, *args, **kwargs):
        context_temp = {'name':'hosts','children':[]}
        for h in HOSTS:
            host = {'ip':h}
            context_temp['children'].append(host)
        host_list = context_temp['children']
        context = {'hosts_list': host_list}
        return context


class StatisticsTab(tabs.Tab):
    name = _("Host Statistics")
    slug = "host_statistics"
    template_name = ("admin/availability/host_statistics.html")
   
    def get_context_data(self, request, *args, **kwargs):
        context = template.RequestContext(request)
        return context

class ServiceTab(tabs.Tab):
    name = _("Service")
    slug = "service"
    template_name = ("admin/availability/service.html")

    def get_context_data(self, request, *args, **kwargs):
        context_temp = {'name':'hosts', 'children':[]}
        for h in HOSTS:
            host = {'ip':h}
            context_temp['children'].append(host)
        host_list = context_temp['children']
        context = {'hosts_list': host_list}
        return context


class AvailabilityOverview(tabs.TabGroup):
    slug = "availability_overview"
    tabs = (HostTab, StatisticsTab, ServiceTab, )
    sticky = True
