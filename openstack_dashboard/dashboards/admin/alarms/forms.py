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

from openstack_dashboard import api


class AddAlarmForm(forms.SelfHandlingForm):
    alarm_name = forms.CharField(label=_("Alarm Name"),
                           max_length=64)
    threshold = forms.IntegerField(label=_("Threshold"),
                           )
    evaluation_period = forms.IntegerField(label=_("Evaluation Period"),
                           )
    resource = forms.ChoiceField(label=_("Resource"),
                           choices=[('cpu_util', _('cpu_util'))])
    operator = forms.ChoiceField(label=_("Operator"),
                           choices=[('greater', _('greater')), ('less', _('less'))])
    time = forms.IntegerField(label=_("Time"),
                           )

    def handle(self, request, data):
        return False
