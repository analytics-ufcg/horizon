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

from horizon import forms
from horizon import tabs

from openstack_dashboard import api

from openstack_dashboard.dashboards.admin.alarms import tabs as \
    alarms_tabs
from openstack_dashboard.dashboards.admin.alarms import forms as \
    alarms_forms

import requests

class IndexView(tabs.TabbedTableView):
    tab_group_class = alarms_tabs.AlarmsOverviewTabs
    template_name = 'admin/alarms/index.html'

class AddAlarmView(forms.ModalFormView):
    template_name = 'admin/alarms/create.html'
    form_class = alarms_forms.AddAlarmForm
    success_url = 'horizon:admin:alarms:index'

    def get_success_url(self):
        return 'horizon:admin:alarms:index'
