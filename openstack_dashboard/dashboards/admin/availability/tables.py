from django.utils import text
from django.utils.translation import ugettext_lazy as _

from horizon import tables


class HostAvailabilityTable(tables.DataTable):
    host = tables.Column('host', verbose_name=_('Host'))
    mtbf = tables.Column('mtbf', verbose_name=_('MTBF'))
    mttr = tables.Column('mttr', verbose_name=_('MTTR'))
    max_time_up = tables.Column('max_time_up', verbose_name=_('Max Time Up'))
    avg_time_up = tables.Column('avg_time_up', verbose_name=_('Average Time Up'))
    std_time_up = tables.Column('std_time_up', verbose_name=_('Standart Deviation Time Up'))
    availability_percent = tables.Column('availability_percent', verbose_name=_('Availability rate'))
    #second_quantile = tables.Column('second', verbose_name=_('Second Quartile'))
    #third_quantile = tables.Column('third', verbose_name=_('First Quartile'))
    #fourth_quantile = tables.Column('fourth', verbose_name=_('Fourth Quartile'))

    def get_object_id(self, obj):
        return '%s' % (obj.host) 

    #def __unicode__(self):
        #return self.title

    class Meta:
        name = "host_availability"
        verbose_name = _("Host Availability - (in hours)")
