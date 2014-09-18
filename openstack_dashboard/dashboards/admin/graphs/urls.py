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

from django.conf.urls import patterns  # noqa
from django.conf.urls import url  # noqa

from openstack_dashboard.dashboards.admin.graphs import views

urlpatterns = patterns('openstack_dashboard.dashboards.admin.graphs.views',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^hosts$', views.HostView.as_view(), name='hosts'),
    url(r'^aggregates$',views.AggregatesView.as_view(),name='aggregates'),
    url(r'^vcpus_for_aggregate$',views.AggregatesVcpuView.as_view(),name='vcpus_for_aggregate'),
    url(r'^projects$',views.ProjectsView.as_view(),name='projects'),
)
