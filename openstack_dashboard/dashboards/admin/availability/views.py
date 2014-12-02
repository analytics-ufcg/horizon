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

import json
from django.http import HttpResponse

from datetime import datetime  # noqa
from datetime import timedelta  # noqa

import pytz
from horizon import tabs
from horizon import tables

from openstack_dashboard.dashboards.admin.availability import tabs as \
    availability_tabs

from openstack_dashboard.dashboards.admin.availability import tables as \
    availability_tables

from openstack_dashboard.api.telemetry_api.telemetry_data \
    import DataHandler


class IndexView(tabs.TabbedTableView):
    tab_group_class = availability_tabs.AvailabilityOverview
    template_name = 'admin/availability/index.html'


class HostGraphView(TemplateView):
    template_name = 'admin/availability/host.html'

    def get(self, request, *args, **kwargs):
        # get url parameters
        times_begin = request.GET.get('timestamp_begin')
        times_end = request.GET.get('timestamp_end')
        host = request.GET.get('host')

        # get db data
        data_handler = DataHandler()
        json_graf = data_handler.points_reduction_host_status(host, times_begin, times_end)

        return HttpResponse(json.dumps(json_graf), content_type='application/json')


class ServiceGraphView(TemplateView):
    template_name = 'admin/availability/service.html'

    def get(self, request, *args, **kwargs):
        # get url parameters
        times_begin = request.GET.get('timestamp_begin')
        times_end = request.GET.get('timestamp_end')
        host = request.GET.get('host')

        # get db data
        data_handler = DataHandler()
        json_graf = data_handler.points_reduction_services_status(host, times_begin, times_end)
        print json_graf
        return HttpResponse(json.dumps(json_graf), content_type='application/json')


class HostStatisticsView(tables.MultiTableView):
    template_name = 'admin/availability/host_statistics_table.html'

    def get_tables(self):
        if self._tables:
            return self._tables

        host_statistics = self.load_data(self.request)
        table_instances = []
        table = availability_tables.HostAvailabilityTable(self.request,
                                                  data=host_statistics,
                                                  kwargs=self.kwargs.copy())
        table.title = 'table 1'
        t = (table.name, table)
        table_instances.append(t)

        self._tables = SortedDict(table_instances)
        return self._tables

    def handle_table(self, table):
        name = table.name
        handled = self._tables[name].maybe_handle()
        return handled

    def load_data(self, request):
        #get data handler instance
        data_handler = DataHandler()

        #get date options
        self.date_options = request.POST.get('date_options', None)
        date_from = request.POST.get('date_from', None)
        date_to = request.POST.get('date_to', None)
        
        date_from, date_to = _calc_date_args(date_from, date_to, self.date_options)

        #get metrics
        host_availability_metrics = data_handler.get_host_availability_metrics(date_from, date_to)

        self.hosts_metrics_list = []
        for host_result_obj in host_availability_metrics:
            self.hosts_metrics_list.append(host_result_obj.to_dict())

        return host_availability_metrics

    def get_context_data(self, **kwargs):
        context = {}
        context['tables'] = self.get_tables().values()
        context['hosts_metrics_list'] = self.hosts_metrics_list

        # map the inputs to the function blocks
        options = {
                   '0' : 'Last Hour',
                   '1' : 'Last Day',
                   '7' : 'Last Week',
                   '30' : 'Last Month',
                   '365': 'Last Year',
                   'other' : 'other',
                  }
        context['date_option'] = options[self.date_options]
        return context


def _calc_date_args(date_from, date_to, date_options):
    # TODO(lsmola) all timestamps should probably work with
    # current timezone. And also show the current timezone in chart.
    if (date_options == "other"):
        try:
            if date_from:
                date_from = datetime.strptime(date_from,
                                              "%Y-%m-%d")
            else:
                # TODO(lsmola) there should be probably the date
                # of the first sample as default, so it correctly
                # counts the time window. Though I need ordering
                # and limit of samples to obtain that.
                pass
            if date_to:
                date_to = datetime.strptime(date_to,
                                            "%Y-%m-%d")
                # It return beginning of the day, I want the and of
                # the day, so i will add one day without a second.
                date_to = (date_to + timedelta(days=1) -
                           timedelta(seconds=1))
            else:
                date_to = datetime.now()
        except Exception:
            raise ValueError("The dates haven't been "
                             "recognized")
    elif (int(date_options) == 0):
        print '---' + date_options
        try:
            date_from = datetime.now() + timedelta(days=0, hours=-1)
            date_to = datetime.now()
        except Exception:
            raise ValueError("The time delta must be an "
                             "integer representing days.")
    else:
        try:
            date_from = datetime.now() - timedelta(days=int(date_options))
            date_to = datetime.now()
        except Exception:
            raise ValueError("The time delta must be an "
                             "integer representing days.")

    # fixme 
    date_from = date_from + timedelta(days=0, hours=-3)
    date_to = date_to + timedelta(days=0, hours=-3)

    return date_from.strftime("%Y-%m-%dT%H:%M:%S"), date_to.strftime("%Y-%m-%dT%H:%M:%S")
