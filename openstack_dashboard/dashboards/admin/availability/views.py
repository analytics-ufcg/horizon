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

from django.views.generic import TemplateView # noqa
from django.utils.datastructures import SortedDict

from horizon import tabs
from horizon import tables

from openstack_dashboard.dashboards.admin.availability import tabs as \
    availability_tabs

from openstack_dashboard.dashboards.admin.availability import tables as \
    availability_tables

class IndexView(tabs.TabbedTableView):
    tab_group_class = availability_tabs.AvailabilityOverview
    template_name = 'admin/availability/index.html'


class HostView(tables.DataTableView):
    table_class = availability_tables.HostAvailabilityTable
    template_name = ""

    def __init__(self, *args, **kwargs):
        super(HostView, self).__init__(*args, **kwargs)


class HostStatisticsView(tables.MultiTableView):
    template_name = 'admin/availability/host_statistics_table.html'

    def get_tables(self):
        if self._tables:
            return self._tables

        host_statistics = self.load_data(self.request)
        table_instances = []
        table = availability_tables.HostAvailabilityTable(self.request, data=host_statistics, kwargs=self.kwargs.copy())
        table.title = 'table 1'
        t = (table.name, table)
        table_instances.append(t)
        
        self._tables = SortedDict(table_instances)
        self.host_statistics = host_statistics
        return self._tables

    def handle_table(self, table):
        name = table.name
        handled = self._tables[name].maybe_handle()
        return handled

    def load_data(self, request):
        date_options = request.POST.get('date_options', None)
        date_from = request.POST.get('date_from', None)
        date_to = request.POST.get('date_to', None)

        host_rows = {}
        row = {"host": 'KKKKKK'}

        host_rows['1'] = row
        return host_rows

    def get_context_data(self, **kwargs):
        context = {}
        context['tables'] = self.get_tables().values()
        return context




