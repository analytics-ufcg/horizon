# Copyright 2014, Analytics/UFCG
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

from openstack_dashboard.api.telemetry import AlarmsHistory as alarms_hist
from openstack_dashboard.api.telemetry import AlarmsList as alarms_list
from openstack_dashboard.dashboards.admin.alarms import tables

from horizon import tabs

import json
import ConfigParser
import time
import datetime

from openstack_dashboard.api.telemetry_api.telemetry_data import DataHandler


class AlarmsListTab(tabs.TableTab):
    table_classes = (tables.AlarmsListTable,)
    name = _("Alarms List")
    slug = "alarms_list"
    template_name = ("horizon/common/_detail_table.html")

    def get_alarms_list_data(self):
        alarms_obj = []

        data_handler = DataHandler()

        alarms_dict = data_handler.alarm_description() 

        for ids in alarms_dict.keys():
            alarm_id = ids
            alarm_name = alarms_dict[ids][0]
            enabled = alarms_dict[ids][1]
            description = alarms_dict[ids][2]
            alarm = alarms_list(ids, alarm_name, enabled, description)
            alarms_obj.append(alarm)
            
        return alarms_obj        


class AlarmsHistoryTab(tabs.TableTab):
    table_classes = (tables.AlarmsHistoryTable,)
    name = _("Alarms History")
    slug = "alarms_history"
    template_name = ("horizon/common/_detail_table.html")

    def get_alarms_history_data(self):
        period = tables.TIME
        alarms_obj = []
        data_handler = DataHandler()
        ts = time.time()

        timestamp_begin = datetime.datetime.fromtimestamp(ts - 
                          (period)).strftime('%Y-%m-%d %H:%M:%S')
        
        timestamp_end = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        alarms_dict = data_handler.alarms_history(timestamp_begin, timestamp_end)

        for data in alarms_dict:
            alarm_name = data['alarm_name']

            for data_history in data['history']:
                timestamp = self.format_timestamp(data_history['timestamp'])

                resource_id = data['resource_id']
                if (resource_id is None): resource_id = 'All'

                detail_str = json.loads(data_history['detail'])
                alarm = alarms_hist(timestamp, alarm_name,
                                    resource_id, 'Current State: ' + detail_str['state'])
                alarms_obj.append(alarm)

        return alarms_obj

    def format_timestamp(self, timestamp):
        date = timestamp[0:10]
        time = timestamp[11:19]
        return date + ' ' + time


class AlarmsOverviewTabs(tabs.TabGroup):
    slug = "alarms_overview"
    tabs = (AlarmsListTab, AlarmsHistoryTab,)
    sticky = True
