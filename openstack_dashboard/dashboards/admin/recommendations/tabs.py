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
 
import requests

class UpgradesTab(tabs.TableTab):
    table_classes = (tables.UpgradeTable,)
    name = _("Upgrades")
    slug = "upgrades"
    template_name = ("horizon/common/_detail_table.html")
    #recommendations/upgrades.html")

    def get_upgrades_data(self):
        req = requests.get("http://150.165.15.4:9090/host_metrics?project=demo")
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

class PowerTab(tabs.Tab):
    name = _("Power Saving")
    slug = "power"
    template_name = ("admin/recommendations/power.html")

    def get_context_data(self, request):
        return None 

class RecommendationsTabs(tabs.TabGroup):
    slug = "recommendations_overview"
    tabs = (UpgradesTab, FlavorsTab, PowerTab, )
    sticky = True
