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


from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView  # noqa
from django.shortcuts import render

from horizon import tables

from openstack_dashboard.dashboards.admin.benchmark import tables as project_tables

from openstack_dashboard.api.telemetry import BenchmarkMemory as benchMemory 
from openstack_dashboard.api.telemetry import BenchmarkCpu as benchCpu 
from openstack_dashboard.api.telemetry import BenchmarkDisk as benchDisk

import requests

class IndexView(tables.MultiTableView):
    table_classes = (project_tables.BenchmarkCpuTable, project_tables.BenchmarkMemoryTable, project_tables.BenchmarkDiskTable)
    template_name = 'admin/benchmark/index.html'
    req_benchmark = requests.get("http://150.165.15.4:9090/benchmark_data")

    def get_data(self):
        return []

    def get_cpu_data(self):
        cpu_data = []
        if self.req_benchmark.status_code == 200:
            lista = self.req_benchmark.json()
            if len(lista) > 0:
                for dic in lista:
                    row = benchCpu(dic['host'], dic['cpu_average'], dic['cpu_median'], dic['cpu_min'], dic['cpu_max'], dic['cpu_first_quarter'],dic['cpu_second_quarter'], dic['cpu_third_quarter'], dic['cpu_fourth_quarter'])
                    cpu_data.append(row)
            else:
                return cpu_data

        return cpu_data

    def get_disk_data(self):
        disk_data = []
        if self.req_benchmark.status_code == 200:
            lista = self.req_benchmark.json()
            if len(lista) > 0:
                for dic in lista:
                    row = benchCpu(dic['host'], dic['disk_average'], dic['disk_median'], dic['disk_min'], dic['disk_max'],dic['disk_first_quarter'],dic['disk_second_quarter'],dic['disk_third_quarter'],dic['disk_fourth_quarter'])
                    disk_data.append(row)
            else:
                return disk_data

        return disk_data

    def get_memory_data(self):
        memory_data = []
        if self.req_benchmark.status_code == 200:
            lista = self.req_benchmark.json()
            if len(lista) > 0:
                for dic in lista:
                    row = benchCpu(dic['host'], dic['mem_average'], dic['mem_median'], dic['mem_min'], dic['mem_max'], dic['mem_first_quarter'], dic['mem_second_quarter'], dic['mem_third_quarter'], dic['mem_fourth_quarter'])
                    memory_data.append(row)
            else:
                return memory_data

        return memory_data
