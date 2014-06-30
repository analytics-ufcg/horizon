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

from horizon import exceptions
from horizon import forms
from horizon import messages

from openstack_dashboard.api.telemetry import AlarmsList as alarms_list

from openstack_dashboard import api

import requests

class AddAlarmForm(forms.SelfHandlingForm):
    name = forms.CharField(label=_("Alarm Name"),
                           max_length=64, help_text=_("Field to input the Alarm Name"))
    threshold = forms.IntegerField(label=_("Threshold"), help_text=_("The value of metric you want to compare"),
                           )
    evalperiod = forms.IntegerField(label=_("Evaluation Period"), help_text=_("Evaluation Period"),
                           )
    resource = forms.ChoiceField(label=_("Resource"), help_text=_("The metric"),
                           choices=[('cpu_util', _('cpu_util'))])
    operator = forms.ChoiceField(label=_("Operator"), help_text=_("Greater than threshold or less"),
                           choices=[('gt', _('greater')), ('lt', _('less'))])
    period = forms.IntegerField(label=_("Time"), help_text=_("Time"),
                           )

    def handle(self, request, data):
        r = requests.post("http://150.165.15.4:9090/add_alarm?name=%s&resource=%s&threshold=%d&operator=%s&period=%d&evalperiod=%d" % (data['name'], data['resource'], data['threshold'], data['operator'], data['period'], data['evalperiod']))
        return True
