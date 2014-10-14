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

from django.utils.translation import ugettext_lazy as _

from horizon import tables

from openstack_dashboard.api.telemetry \
    import SentMessages as sent_messages

from openstack_dashboard.dashboards.admin.sent_messages \
    import tables as sent_tables


class IndexView(tables.DataTableView):
    table_class = sent_tables.SentTable
    template_name = 'admin/sent_messages/index.html'

    def get_data(self):
        sent_data = []
        return sent_data
