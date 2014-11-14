from django.utils import text

from django.core.urlresolvers import reverse
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _

from horizon import tables


class HostAvailabilityTable(tables.DataTable):
    id = tables.Column('id', hidden=True)
    #name = tables.Column("name", verbose_name=_('Membro'))
    #multas = tables.Column('multas', verbose_name=_('Quantidade de Multas'))
    host = tables.Column('host', verbose_name=_('Host'))
    avg = tables.Column('avg', verbose_name=_('Average'))
    median = tables.Column('median', verbose_name=_('Median'))
    min = tables.Column('min', verbose_name=_('Min'))
    max = tables.Column('max', verbose_name=_('Max'))
    #first_quantile = tables.Column('first', verbose_name=_('First Quartile'))
    #second_quantile = tables.Column('second', verbose_name=_('Second Quartile'))
    #third_quantile = tables.Column('third', verbose_name=_('First Quartile'))
    #fourth_quantile = tables.Column('fourth', verbose_name=_('Fourth Quartile'))

    #def get_object_id(self, obj):
        #return '%s' % (obj.host)
        #return 'obj_id' 

    #def __unicode__(self):
        #return self.title

    class Meta:
        name = "host_availability"
        verbose_name = _("Host Availability")
