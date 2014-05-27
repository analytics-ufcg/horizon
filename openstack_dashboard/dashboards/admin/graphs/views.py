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

from django.views.generic import TemplateView  # noqa
from django.shortcuts import render

from horizon import tabs

from openstack_dashboard.dashboards.admin.graphs import tabs as \
    graphs_tabs

import requests, json

class IndexView(tabs.TabView):
    tab_group_class = graphs_tabs.GraphsTabs
    template_name = 'admin/graphs/index.html'


class HostView(TemplateView):
    template_name = 'admin/graphs/hosts.html'

    def get(self, request, *args, **kwargs):
        r = requests.get('http://localhost:9090/hosts')
        context = {}
        if r.status_code == 200:
            context['hosts_list'] = r.json()['children']
        return context

