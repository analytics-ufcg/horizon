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

from django.utils.translation import ugettext_lazy as _

from horizon import tabs

from openstack_dashboard.api.telemetry \
    import RecommendationMigration as dataMigration
from openstack_dashboard.api.telemetry \
    import RecommendationPowerStatus as dataStatus
from openstack_dashboard.api.telemetry \
    import RecommendationUpgrade as dataUpgrade
from openstack_dashboard.dashboards.admin.recommendations \
    import tables

import requests

from openstack_dashboard.api.telemetry_api.telemetry_data import DataHandler

class UpgradesTab(tabs.TableTab):
    table_classes = (tables.UpgradeTable,)
    name = _("Upgrades")
    slug = "upgrades"
    template_name = ("horizon/common/_detail_table.html")
    #recommendations/upgrades.html")

    def get_upgrades_data(self):
        upgrade_list = []
        data_handler = DataHandler()
        data = data_handler.host_metrics('admin') 
        for h in data.keys():
            host = dataUpgrade(h, data[h]['Total'][0],
                               data[h]['Em uso'][0],
                               data[h]['Percentual'][0],
                               data[h]['Total'][1],
                               data[h]['Em uso'][1],
                               data[h]['Percentual'][1],
                               data[h]['Total'][2],
                               data[h]['Em uso'][2],
                               data[h]['Percentual'][2])
            upgrade_list.append(host)
        return upgrade_list


class FlavorsTab(tabs.Tab):
    #table_classes = (tables.FlavorTable,)
    name = _("Flavors")
    slug = "flavors_rec"
    #template_name = ("horizon/common/_detail_table.html")
    template_name = ("admin/recommendations/flavors.html")

    def get_context_data(self, request):
        #req = requests.get("http://150.165.15.4:9090/o")
        #flavor_list = []
        #if req.status_code == 200:
        #    data = req.json()

        #return flavor_list
        return None


class PowerTab(tabs.TableTab):
    table_classes = (tables.StatusTable, tables.MigrationTable,)
    name = _("Power Saving")
    slug = "power"
    template_name = ("admin/recommendations/power.html")
    host_migration_data = None

    def get_status_data(self):
        hosts_list = tables.HOSTS
        host_status = []

        data_handler = DataHandler()

        if self.host_migration_data is None:
            self.host_migration_data = data_handler.suggestion(hosts_list)

	data = self.host_migration_data['Hosts']
	for k in data.keys():
	    if data[k] is True:
		row = dataStatus(k, "Shut Off")
	    else:
		row = dataStatus(k, "Keep On")
	    host_status.append(row)
        
	return host_status

    def get_migration_data(self):
        hosts_list = tables.HOSTS
        hosts = {}
        migration = []
        flag = False

        data_handler = DataHandler()

        if self.host_migration_data is None:
            self.host_migration_data = data_handler.suggestion(hosts_list)

	data = self.host_migration_data['Migracoes']
	for k in data.keys():
            for vm in data[k]:
		if data[k][vm] is not None:
		    flag = True

		    if k not in hosts:
		       hosts[k] = {'server': [], 'name': [],
				   'endhost': [], 'project': []}

		    hosts[k]['server'].append(vm)
		    hosts[k]['name'].append(data[k][vm][1])
		    hosts[k]['endhost'].append(data[k][vm][0])
		    hosts[k]['project'].append(data[k][vm][2])

	    if flag:
		row = dataMigration(k,
				    hosts[k]['server'],
				    hosts[k]['name'],
				    hosts[k]['endhost'],
				    hosts[k]['project'])
		migration.append(row)
		flag = False

            if hosts_list is not []:
                hosts_list = []
                tables.HOSTS = []
        
        return migration


class RecommendationsTabs(tabs.TabGroup):
    slug = "recommendations_overview"
    tabs = (UpgradesTab, FlavorsTab, PowerTab,)
    sticky = True
