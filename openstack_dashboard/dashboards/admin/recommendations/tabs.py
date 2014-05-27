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

class UpgradesTab(tabs.Tab):
    name = _("Upgrades")
    slug = "upgrades"
    template_name = ("admin/recommendations/upgrades.html")

    def get_context_data(self, request):
        return None

class FlavorsTab(tabs.Tab):
    name = _("Flavors")
    slug = "flavors_rec"
    template_name = ("admin/recommendations/flavors.html")
    preload = False

    def get_context_data(self, request):
        return None

class PowerTab(tabs.Tab):
    name = _("Power Saving")
    slug = "power"
    template_name = ("admin/recommendations/power.html")
    preload = False

    def get_context_data(self, request):
        return None 

class RecommendationsTabs(tabs.TabGroup):
    slug = "recommendations_overview"
    tabs = (UpgradesTab, FlavorsTab, PowerTab, )
    sticky = True
