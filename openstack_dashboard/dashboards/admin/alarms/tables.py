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
from django.template import defaultfilters as filters
from django.utils.translation import ugettext_lazy as _

from horizon import tables

from horizon.templatetags import sizeformat

class AlarmsHistoryTable(tables.DataTable):
    timestamp = tables.Column("timestamp", verbose_name=_('TimeStamp'))
    alarm_name = tables.Column('alarm_name', verbose_name=_('Alarm Name'))
    alarm_type = tables.Column('alarm_type', verbose_name=_('Type'))
    detail = tables.Column('detail', verbose_name=_('Detail'))
    
    def get_object_id(self, obj):
        return "%s" % (obj.alarm_name)
    
    class Meta:
        name = "alarms_history"
        verbose_name = _("Alarm History")
        multi_select = False


class AlarmsListTable(tables.DataTable):
    alarm_name = tables.Column("alarm_name", verbose_name=_('Alarm Name'))
    alarm_id = tables.Column('alarm_id', verbose_name=_('Alarm Id'))
    enabled = tables.Column('enabled', verbose_name=_('Enabled'))
    description = tables.Column('description', verbose_name=_('Description'))

    def get_object_id(self, obj):
        return "%s" % (obj.alarm_id)

    class Meta:
        name = "alarms_list"
        verbose_name = _("Alarms List")
        multi_select = False


