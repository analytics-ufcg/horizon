# Copyright 2014, Analytics/UFCG
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

from horizon import tables

from openstack_dashboard.dashboards.admin.benchmark \
    import tables as project_tables

from openstack_dashboard.api.telemetry \
    import BenchmarkCpu as benchCpu
from openstack_dashboard.api.telemetry \
    import BenchmarkDisk as benchDisk
from openstack_dashboard.api.telemetry \
    import BenchmarkMemory as benchMemory

from openstack_dashboard.api.telemetry_api.telemetry_data \
    import DataHandler

class IndexView(tables.MultiTableView):
    table_classes = (project_tables.BenchmarkCpuTable,
                     project_tables.BenchmarkMemoryTable,
                     project_tables.BenchmarkDiskTable)
    template_name = 'admin/benchmark/index.html'
    benchmark_data = None

    def get_data(self):
        return []

    def get_cpu_data(self):
        cpu_data = []
        data_handler = DataHandler()

        if self.benchmark_data is None:
            self.benchmark_data = data_handler.get_benchmark_bd()

	lista = self.benchmark_data
	if len(lista) > 0:
	    for dic in lista:
		row = benchCpu(dic['host'], dic['cpu_average'],
			       dic['cpu_median'], dic['cpu_min'],
			       dic['cpu_max'], dic['cpu_first_quarter'],
			       dic['cpu_second_quarter'],
			       dic['cpu_third_quarter'],
			       dic['cpu_fourth_quarter'])
		cpu_data.append(row)
	else:
	    return cpu_data

        return cpu_data

    def get_disk_data(self):
        disk_data = []
        data_handler = DataHandler()

        if self.benchmark_data is None:
            self.benchmark_data = data_handler.get_benchmark_bd()

	lista = self.benchmark_data
	if len(lista) > 0:
	    for dic in lista:
		row = benchDisk(dic['host'], dic['disk_average'],
				dic['disk_median'], dic['disk_min'],
				dic['disk_max'],
				dic['disk_first_quarter'],
				dic['disk_second_quarter'],
				dic['disk_third_quarter'],
				dic['disk_fourth_quarter'])
		disk_data.append(row)
	else:
	    return disk_data

        return disk_data

    def get_memory_data(self):
        memory_data = []
        data_handler = DataHandler()

        if self.benchmark_data is None:
            self.benchmark_data = data_handler.get_benchmark_bd()

	lista = self.benchmark_data
	if len(lista) > 0:
	    for dic in lista:
		row = benchMemory(dic['host'], dic['mem_average'],
				  dic['mem_median'], dic['mem_min'],
				  dic['mem_max'],
				  dic['mem_first_quarter'],
				  dic['mem_second_quarter'],
				  dic['mem_third_quarter'],
				  dic['mem_fourth_quarter'])
		memory_data.append(row)
	else:
	    return memory_data

        return memory_data
