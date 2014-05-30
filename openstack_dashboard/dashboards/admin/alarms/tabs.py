# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from django import template
from django.utils.translation import ugettext_lazy as _

from openstack_dashboard.api import keystone

from horizon import tabs

from openstack_dashboard.dashboards.admin.alarms import tables

class AlarmHistoryTab(tabs.Tab):
    name = _("Alarm History")
    slug = "alarm_history"
    template_name = ("horizon/common/_detail_table.html")

    def get_context_data(self, request):
        return None

class AlarmsListTab(tabs.TableTab):
    table_classes = (tables.AlarmsListTable,)
    name = _("Alarms List")
    slug = "alarms_list"
    template_name = ("horizon/common/_detail_table.html")

    def get_alarms_list_data(self):
        request = self.tab_group.request
        services = []
        return services

class AlarmsOverviewTabs(tabs.TabGroup):
    slug = "alarms_overview"
    tabs = (AlarmHistoryTab, AlarmsListTab, )
    sticky = True
