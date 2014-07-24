# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 B1 Systems GmbH
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

import requests


class AlarmsHistoryFilterAction(tables.FilterAction):
    def filter(self, alarms_history, filter_string):
        q = filter_string.lower()

        def comp(alarms_history):
            if q in alarms_history.type.lower():
                return True
            return False
        return filter(comp, alarms_history)


class AlarmsHistoryTable(tables.DataTable):
    timestamp = tables.Column("timestamp",
                              verbose_name=_('TimeStamp'))
    alarm_name = tables.Column('alarm_name',
                               verbose_name=_('Alarm Name'))
    alarm_type = tables.Column('alarm_type',
                               verbose_name=_('Type'))
    detail = tables.Column('detail',
                           verbose_name=_('Detail'))

    def get_object_id(self, obj):
        return "%s-%s" % (obj.timestamp, obj.alarm_name)

    class Meta:
        name = "alarms_history"
        verbose_name = _("Alarm History")
        table_actions = (AlarmsHistoryFilterAction,)
        multi_select = False


class DeleteAlarmsAction(tables.DeleteAction):
    data_type_singular = _("Alarm")
    data_type_plural = _("Alarms")

    def delete(self, request, obj_id):
        requests.post("http://150.165.15.104:10090/alarm_delete?alarm_id=" + obj_id)


class CreateAlarmsAction(tables.LinkAction):
    name = "create_alarm"
    verbose_name = _("Create Alarm")
    url = "horizon:admin:alarms:create"
    classes = ("btn-launch", "ajax-modal")


class AlarmsListFilterAction(tables.FilterAction):
    def filter(self, alarms_list, filter_string):
        q = filter_string.lower()

        def comp(alarms_list):
            if q in alarms_list.type.lower():
                return True
            return False
        return filter(comp, alarms_list)


class AlarmsListTable(tables.DataTable):
    alarm_name = tables.Column("alarm_name",
                               verbose_name=_('Alarm Name'))
    alarm_id = tables.Column('alarm_id',
                             verbose_name=_('Alarm Id'))
    enabled = tables.Column('enabled',
                            verbose_name=_('Enabled'))
    description = tables.Column('description',
                                verbose_name=_('Description'))

    def get_object_id(self, obj):
        return "%s" % (obj.alarm_id)

    def get_object_display(self, obj):
        return "%s" % (obj.alarm_name)

    class Meta:
        name = "alarms_list"
        verbose_name = _("Alarms List")
        rows_actions = (DeleteAlarmsAction)
        table_actions = (AlarmsListFilterAction,
                         CreateAlarmsAction,
                         DeleteAlarmsAction,)
