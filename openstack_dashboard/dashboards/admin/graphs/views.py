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

from django.views.generic import TemplateView  # noqa

from horizon import tabs
import json
from django.http import HttpResponse
from openstack_dashboard.dashboards.admin.graphs import tabs as \
    graphs_tabs

from openstack_dashboard.api.telemetry_api.telemetry_data import DataHandler
import requests, threading, ConfigParser, ast

class IndexView(tabs.TabView):
    tab_group_class = graphs_tabs.GraphsTabs
    template_name = 'admin/graphs/index.html'

class HostView(TemplateView):
    template_name = 'admin/graphs/host.html'

    def get(self, request, *args, **kwargs):
        data_handler = DataHandler()
        HOSTS = ast.literal_eval(data_handler.get_config().get('Openstack', 'computenodes'))
        template_name = 'admin/graphs/host.html'
        times_begin = request.GET.get('timestamp_begin')
        times_end = request.GET.get('timestamp_end')
        meter = request.GET.get('meter')

        json_graf = None
        if(meter == 'cpu'):
            json_graf = data_handler.points_reduction_by_server_cpu(timestamp_begin=times_begin, timestamp_end=times_end,hosts=HOSTS)
        elif(meter == 'disk'):
            json_graf = data_handler.points_reduction_by_server_disk(timestamp_begin=times_begin, timestamp_end=times_end,hosts=HOSTS)
        elif(meter == 'memory'):
            json_graf = data_handler.points_reduction_by_server_memory(timestamp_begin=times_begin, timestamp_end=times_end,hosts=HOSTS)
        elif(meter == 'network'):
            json_graf = data_handler.points_reduction_by_server_network(timestamp_begin=times_begin, timestamp_end=times_end,hosts=HOSTS)

        return HttpResponse(json.dumps(json_graf), content_type='application/json')

class AggregatesView(TemplateView):
    template_name = 'admin/graphs/aggregates.html'
    
    def get(self, request):
        data_handler = DataHandler()
        times_begin = request.GET.get('timestamp_begin')
        times_end = request.GET.get('timestamp_end')
        meter = request.GET.get('meter')

        json_graf = None
        if(meter == 'cpu'):
            json_graf = data_handler.hosts_aggregation_cpu(timestamp_begin=times_begin, timestamp_end=times_end)
        elif(meter == 'memory'):
            json_graf = data_handler.hosts_aggregation_memory(timestamp_begin=times_begin, timestamp_end=times_end)
        elif(meter == 'disk'):
            json_graf = data_handler.hosts_aggregation_disk(timestamp_begin=times_begin, timestamp_end=times_end)
        elif(meter == 'network'):
            json_graf = data_handler.hosts_aggregation_network(timestamp_begin=times_begin, timestamp_end=times_end)

        return HttpResponse(json_graf)

class AggregatesVcpuView(TemplateView):
    template_name = 'admin/graphs/aggregates.html'

    def get(self, request):
        project_name = request.GET.get('project')
        data_handler = DataHandler()
        json_graf = data_handler.vcpus_for_aggregate(project_name)
        print "resposta de Vcpus: " + str(json_graf)
        return HttpResponse(json_graf)

class ProjectsView(TemplateView):
    template_name = 'admin/graphs/projects.html'
    
    def get(self,request):
        times_begin = request.GET.get('timestamp_begin')
        times_end = request.GET.get('timestamp_end')
        r_id = request.GET.get('resource_id')
        meter = request.GET.get('meter')
        data_handler = DataHandler()

        json_graf = None

        if meter == "cpu":
            json_graf = json.dumps(data_handler.points_reduction_vm(timestamp_begin=times_begin, timestamp_end=times_end,resource_id=r_id))

        if meter == "network":
            network_incoming_bytes_rate = data_handler.points_reduction_vm_network_incoming(timestamp_begin=times_begin, timestamp_end=times_end,resource_id=r_id);
            network_outgoing_bytes_rate = data_handler.points_reduction_vm_network_outgoing(timestamp_begin=times_begin, timestamp_end=times_end,resource_id=r_id);
            json_graf = json.dumps({'network_incoming': network_incoming_bytes_rate, 'network_outgoing': network_outgoing_bytes_rate})

        return HttpResponse(json_graf)

class CpuUtilFlavorsView(TemplateView):
    template_name = 'admin/recommendations/flavors.html'

    def get(self, request):
        data_handler = DataHandler()
        times_begin = request.GET.get('timestamp_begin')
        times_end = request.GET.get('timestamp_end')
        json_graf = data_handler.cpu_util_flavors(times_begin, times_end)

        return HttpResponse(json_graf)
