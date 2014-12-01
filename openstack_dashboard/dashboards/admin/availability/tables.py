from django.utils import text
from django.utils.translation import ugettext_lazy as _

from horizon import tables


class HostAvailabilityTable(tables.DataTable):
    host = tables.Column('host', verbose_name=_('Host'))
    mtbf = tables.Column('mtbf', verbose_name=_('MTBF'))
    mttr = tables.Column('mttr', verbose_name=_('MTTR'))
    total_up_time = tables.Column('total_up_time', verbose_name=_('Total Up Time'))
    total_down_time = tables.Column('total_down_time', verbose_name=_('Total Down Time'))
    failures_count = tables.Column('failures_count', verbose_name=_('Failures Count'))
    availability_percent = tables.Column('availability_percent', verbose_name=_('Availability rate'))
    begin_time = tables.Column('begin_time', verbose_name = _('Begin timestamp'))

    def get_object_id(self, obj):
        return '%s' % (obj.host) 

    class Meta:
        name = "host_availability"
        verbose_name = _("Host Availability - (in hours)")
