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


class BenchmarkCpuTable(tables.DataTable):
    host = tables.Column('host', verbose_name=_('Host'))
    avg = tables.Column('avg', verbose_name=_('Average'))
    median = tables.Column('median', verbose_name=_('Median'))
    min = tables.Column('min', verbose_name=_('Min'))
    max = tables.Column('max', verbose_name=_('Max'))
    first_quantile = tables.Column('first',
                                   verbose_name=_('First Quartile'))
    second_quantile = tables.Column('second',
                                    verbose_name=_('Second Quartile'))
    third_quantile = tables.Column('third',
                                   verbose_name=_('First Quartile'))
    fourth_quantile = tables.Column('fourth',
                                    verbose_name=_('Fourth Quartile'))

    def get_object_id(self, obj):
        return '%s' % (obj.host)

    class Meta:
        name = "cpu"
        verbose_name = _("CPU")


class BenchmarkMemoryTable(tables.DataTable):
    host = tables.Column('host', verbose_name=_('Host'))
    avg = tables.Column('avg', verbose_name=_('Average'))
    median = tables.Column('median', verbose_name=_('Median'))
    min = tables.Column('min', verbose_name=_('Min'))
    max = tables.Column('max', verbose_name=_('Max'))
    first_quantile = tables.Column('first',
                                   verbose_name=_('First Quartile'))
    second_quantile = tables.Column('second',
                                    verbose_name=_('Second Quartile'))
    third_quantile = tables.Column('third',
                                   verbose_name=_('First Quartile'))
    fourth_quantile = tables.Column('fourth',
                                    verbose_name=_('Fourth Quartile'))

    def get_object_id(self, obj):
        return '%s' % (obj.host)

    class Meta:
        name = "memory"
        verbose_name = _("Memory")


class BenchmarkDiskTable(tables.DataTable):
    host = tables.Column('host', verbose_name=_('Host'))
    avg = tables.Column('avg', verbose_name=_('Average'))
    median = tables.Column('median', verbose_name=_('Median'))
    min = tables.Column('min', verbose_name=_('Min'))
    max = tables.Column('max', verbose_name=_('Max'))
    first_quantile = tables.Column('first',
                                   verbose_name=_('First Quartile'))
    second_quantile = tables.Column('second',
                                    verbose_name=_('Second Quartile'))
    third_quantile = tables.Column('third',
                                   verbose_name=_('First Quartile'))
    fourth_quantile = tables.Column('fourth',
                                    verbose_name=_('Fourth Quartile'))

    def get_object_id(self, obj):
        return '%s' % (obj.host)

    class Meta:
        name = "disk"
        verbose_name = _("Disk")
