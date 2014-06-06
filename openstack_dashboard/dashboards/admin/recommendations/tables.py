from django import template
from django.template import defaultfilters as filters
from django.utils.translation import ugettext_lazy as _

from horizon import tables
from horizon.utils import filters as utils_filters



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
        verbose_name = _("Upgrade")
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
