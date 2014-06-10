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

from django.utils.translation import ugettext_lazy as _

from horizon import tables



class UpgradeFilterAction(tables.FilterAction):
    def filter(self,table, resources, filter_string):
        q = filter_string.lower()
        
        def comp(resource):
            if q in resource.type.lower():
                return True
            return False
        
        return filter(comp,resources)

class UpgradeTable(tables.DataTable):
    host = tables.Column('host', verbose_name=_('Host'))
    cpu_total = tables.Column('cpu_total',verbose_name= _('Total CPU'))
    cpu_usage = tables.Column('cpu_usage',verbose_name=_('CPU usage'))
    mem_total = tables.Column('memory_total',verbose_name=_('Total Memory'))
    mem_usage = tables.Column('memory_usage',verbose_name=_('Memory usage'))
    disk_total = tables.Column('disk_total',verbose_name=('Total Disk'))
    disk_usage = tables.Column('disk_usage',verbose_name=_('Disk usage'))
    cpu_p = tables.Column('cpu_percentage',verbose_name=_('CPU (%)'))
    mem_p = tables.Column('memory_percentage',verbose_name=_('Memory (%)'))
    disk_p = tables.Column('disk_percentage',verbose_name=_('Disk (%)'))

    
    def get_object_id(self, obj):
        return "%s" % (obj.host)

    class Meta:
        name="upgrades"
        verbose_name = _(" ")
        table_actions = (UpgradeFilterAction,)
        multi_select = False


class FlavorTable(tables.DataTable):
    rec = tables.Column('name', verbose_name=_('Recommendation'))
    sugest = tables.Column('sugestion', verbose_name=_('Sugestion'))
    lose = tables.Column('lose', verbose_name=_('Lose (%)'))
    violation = tables.Column('violations', verbose_name=_('Violations (%)'))

    def get_object_id(self,obj):
        return "%s" %(obj.name)
    
    class Meta:
        name="flavors"
        verbose_name = _('Flavors')

class StatusTable(tables.DataTable):
    host = tables.Column('host', verbose_name=_('Host'))
    status = tables.Column('status', verbose_name=_('Status'))

    def get_object_id(self,obj):
        return "%s" %(obj.host)

    class Meta:
        name = "status"
        verbose_name = _("Hosts Power Status")
    

class MigrationTable(tables.DataTable):
    host = tables.Column('host', verbose_name=_('Host'))
    server = tables.Column('server', verbose_name=_('Server'))
    end = tables.Column('endhost', verbose_name=_('New Host'))

    def get_object_id(self,obj):
        return "%s" %(obj.server)

    class Meta:
        name = "migration"
        verbose_name = _("Suggested Server Migrations")

     
