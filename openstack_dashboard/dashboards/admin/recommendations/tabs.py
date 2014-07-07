# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
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
from django.utils.translation import ugettext_lazy as _

from horizon import tabs

from openstack_dashboard.dashboards.admin.recommendations import tables
from openstack_dashboard.api.telemetry import RecommendationsUpgrade as dataUpgrade
from openstack_dashboard.api.telemetry import RecommendataionPowerStatus as dataStatus
from openstack_dashboard.api.telemetry import RecommendationMigration as dataMigration 
import requests

class UpgradesTab(tabs.TableTab):
    table_classes = (tables.UpgradeTable,)
    name = _("Upgrades")
    slug = "upgrades"
    template_name = ("horizon/common/_detail_table.html")
    #recommendations/upgrades.html")

    def get_upgrades_data(self):
        req = requests.get("http://150.165.15.104:10090/host_metrics?project=demo")
        upgrade_list = []
        if req.status_code == 200:
            data = req.json()
            for h in data.keys():
                host = dataUpgrade(h,data[h]['Total'][0],data[h]['Em uso'][0],data[h]['Percentual'][0],data[h]['Total'][1],data[h]['Em uso'][1],data[h]['Percentual'][1],data[h]['Total'][2],data[h]['Em uso'][2],data[h]['Percentual'][2])
                upgrade_list.append(host)
        return  upgrade_list

class FlavorsTab(tabs.Tab):
    #tabs.TableTab
    #table_classes = (tables.FlavorTable,)
    name = _("Flavors")
    slug = "flavors_rec"
    #template_name = ("horizon/common/_detail_table.html")
    template_name = ("admin/recommendations/flavors.html")
    #def get_flavors_data(self):
    def get_context_data(self,request):
        #req = requests.get("http://150.165.15.4:9090/o")
        #flavor_list = []
        #if req.status_code == 200:
        #    data = req.json()
             
        #return flavor_list
        return None

class PowerTab(tabs.TableTab):
    table_classes = ( tables.StatusTable, tables.MigrationTable, ) #tables.StatusTable ,
    name = _("Power Saving")
    slug = "power"
    template_name = ("admin/recommendations/power.html")
    request_host_migration = None

    def get_status_data(self):
        host_status = []

        if self.request_host_migration is None:
            self.request_host_migration = requests.get("http://150.165.15.104:10090/host_migration")

        if self.request_host_migration.status_code == 200:
            data = self.request_host_migration.json()['Hosts']
            for k in data.keys():
                if data[k] == True:
                    row = dataStatus(k,"Shut Off")
                else:
                    row = dataStatus(k,"Keep On")
                host_status.append(row)
        return host_status

    def get_migration_data(self):
        migration = []

        if self.request_host_migration is None:
            self.request_host_migration = requests.get("http://150.165.15.104:10090/host_migration")

        if self.request_host_migration.status_code == 200:
            data = self.request_host_migration.json()['Migracoes']
            for k in data.keys():
                for vm in data[k]:
                    if data[k][vm] != None:
                       row = dataMigration(k,vm,data[k][vm][0],data[k][vm][1])
                       migration.append(row)
        return migration



class RecommendationsTabs(tabs.TabGroup):
    slug = "recommendations_overview"
    tabs = ( UpgradesTab, FlavorsTab, PowerTab, )#UpgradesTab,  FlavorsTab, PowerTab, )
    sticky = True
