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

from django.conf.urls import patterns  # noqa
from django.conf.urls import url  #noqa

from openstack_dashboard.dashboards.admin.availability import views

urlpatterns = patterns('openstack_dashboard.dashboards.admin.availability.views',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^host_graph_data$', views.HostGraphView.as_view(), name='host_graph_data'),
    url(r'^host_statistics$', views.HostStatisticsView.as_view(), name='host_statistics'),
    url(r'^service_graph_data$', views.ServiceGraphView.as_view(), name='service_graph_data')
)
