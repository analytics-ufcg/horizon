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

from django import template
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render

from horizon import tabs

import requests, json

class HostsTab(tabs.Tab):
    name = _("Hosts")
    slug = "hosts"
    template_name = ("admin/graphs/hosts.html")
   
    def get_context_data(self, request, *args, **kwargs):
        r = requests.get('http://150.165.15.4:9090/hosts')
        hosts_list = []

        if r.status_code == 200:
            hosts_list = r.json()['children']
        
        context = { 'hosts_list': hosts_list }
        return context

class AggregatesTab(tabs.Tab):
    name = _("Aggregates")
    slug = "aggregates"
    template_name = ("admin/graphs/aggregates.html")

    def get_context_data(self, request):
        r = requests.get('http://150.165.15.4:9090/hosts_aggregates')
        agg_list = []

        if r.status_code == 200:
            agg_list = r.json()

        context = { 'agg_list': agg_list }
        return context

class ProjectsTab(tabs.Tab):
    name = ("Projects")
    slug = "projects_meter"
    template_name = ("admin/graphs/projects.html")

    def get_context_data(self, request):

        r = requests.get('http://150.165.15.4:9090/projects/instances')
        if r.status_code == 200:
            projs = r.json()['children']
            projects = {}
            for p in projs:
                if len(p['children']) > 0:
                    projects[p['name']] = p['children']
 
        context = {
           'projects': projects,
           'projects_json': json.dumps(projects),
        }

        return context

class GraphsTabs(tabs.TabGroup):
    slug = "graphs_overview"
    tabs =  (HostsTab, ProjectsTab, AggregatesTab, )
    sticky = True

