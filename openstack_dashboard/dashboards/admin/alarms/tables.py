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

import requests

from openstack_dashboard.api.telemetry_api.telemetry_data import DataHandler


TIME = 3600


class AlarmsHistoryFilterAction(tables.FilterAction):
    def filter(self, table, alarms_history, filter_string):
        q = filter_string.lower()

        def comp(alarms_history):
            if q in alarms_history.alarm_name.lower():
                return True
            return False
        return filter(comp, alarms_history)


class UpdateHistoryAction(tables.Action):
    name = "update_history"
    verbose_name = _("Show More (Hour)")
    verbose_name_plural = _("Show More (Hour)")
    preempt = True
    requires_input = False

    def handle(self, data_table, request, obj_ids):
        global TIME
        TIME += 3600


class UpdateHistoryActionDay(tables.Action):
    name = "update_history_day"
    verbose_name = _("Show More (Day)")
    verbose_name_plural = _("Show More (Day)")
    preempt = True
    requires_input = False

    def handle(self, data_table, request, obj_ids):
        global TIME
        TIME += 86400


class ResetHistoryAction(tables.Action):
    name = "reset_button"
    verbose_name = _("Reset")
    verbose_name_plural = _("Reset")
    preempt = True
    requires_input = False

    def handle(self, data_table, request, obj_ids):
        global TIME
        TIME = 3600


class AlarmsHistoryTable(tables.DataTable):
    timestamp = tables.Column("timestamp",
                              verbose_name=_('TimeStamp'))
    alarm_name = tables.Column('alarm_name',
                               verbose_name=_('Alarm Name'))
    resource_id = tables.Column('resource_id',
                               verbose_name=_('Instance ID'))
    detail = tables.Column('detail',
                           verbose_name=_('Detail'))

    def get_object_id(self, obj):
        return "%s-%s" % (obj.timestamp, obj.alarm_name)

    class Meta:
        name = "alarms_history"
        verbose_name = _("Alarm History")
        table_actions = (UpdateHistoryAction,
                         UpdateHistoryActionDay,
                         ResetHistoryAction,
                         AlarmsHistoryFilterAction,)
        multi_select = False


class DeleteAlarmsAction(tables.DeleteAction):
    data_type_singular = _("Alarm")
    data_type_plural = _("Alarms")

    def delete(self, request, obj_id):
        data_handler = DataHandler() 
        data_handler.delete_alarm(obj_id)


class CreateAlarmsAction(tables.LinkAction):
    name = "create_alarm"
    verbose_name = _("Create Alarm")
    url = "horizon:admin:alarms:create"
    classes = ("btn-launch", "ajax-modal")

'''
class AlarmsListFilterAction(tables.FilterAction):
    def filter(self, table, alarms_list, filter_string):
        q = filter_string.lower()

        def comp(alarms_list):
            if q in alarms_list.alarm_name.lower():
                return True
            return False
        return filter(comp, alarms_list)
'''

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
        table_actions = (CreateAlarmsAction,
                         DeleteAlarmsAction,)

