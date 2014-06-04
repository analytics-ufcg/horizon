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

from openstack_dashboard import api
from openstack_dashboard.api.telemetry import AlarmsList as alarms

from horizon import tabs
from horizon import exceptions

from openstack_dashboard.dashboards.admin.alarms import tables
import requests


class AlarmsHistoryTab(tabs.TableTab):
    table_classes = (tables.AlarmsHistoryTable,)
    name = _("Alarms History")
    slug = "alarms_history"
    template_name = ("horizon/common/_detail_table.html")

    def get_alarms_history_data(self):
        request = self.tab_group.request
        services = []
        return services

class AlarmsListTab(tabs.TableTab):
    table_classes = (tables.AlarmsListTable,)
    name = _("Alarms List")
    slug = "alarms_list"
    template_name = ("horizon/common/_detail_table.html")

    def get_alarms_list_data(self):
        r = requests.get('http://localhost:9090/alarm_description')
        alarms_obj = []
        if r.status_code == 200:
            alarms_dict = r.json()
            for ids in alarms_dict.keys():
                alarm_id = ids
                alarm_name = alarms_dict[ids][0]
                enabled = alarms_dict[ids][1]
                description = alarms_dict[ids][2]
                alarm = alarms(ids, alarm_name, enabled, description)
                alarms_obj.append(alarm)
            
        return alarms_obj        

class AlarmsOverviewTabs(tabs.TabGroup):
    slug = "alarms_overview"
    tabs = (AlarmsHistoryTab, AlarmsListTab, )
    sticky = True
