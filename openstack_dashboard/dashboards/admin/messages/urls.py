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

from openstack_dashboard.dashboards.admin.messages import views

urlpatterns = patterns('openstack_dashboard.dashboards.admin.messages.views',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^message_user$', views.MessageUserView.as_view(), name='message_user'),
    url(r'^(?P<id>[^/]+)/message_user$',
        views.MessageUserView.as_view(), name='message_user'),
    url(r'^(?P<id>[^/]+)/message_project$',
        views.MessageProjectView.as_view(), name='message_project'),
    url(r'^(?P<id>[^/]+)/message_host$',
        views.MessageHostView.as_view(), name='message_host'),
)
