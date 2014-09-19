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

from horizon import forms

from openstack_dashboard import api

from openstack_dashboard.api.telemetry_api.telemetry_data import DataHandler

from operator import itemgetter

from horizon import messages

from messages.message_selection import MessageManager

import requests

class AddAlarmForm(forms.SelfHandlingForm):

    name = forms.CharField(label=_("Alarm Name"),
                           max_length=64,
                           help_text=_("Field to input the Alarm Name"))
    threshold = forms.IntegerField(label=_("Threshold"),
                                   help_text=
                                   _("The value of metric to compare"))
    evalperiod = forms.IntegerField(label=_("Evaluation Period"),
                                    help_text=_("Evaluation Period"))
    resource = forms.ChoiceField(label=_("Resource"),
                                 help_text=_("The metric"),
                                 choices=[('cpu_util',
                                          _('cpu_util'))])
    operator = forms.ChoiceField(label=_("Operator"),
                                 help_text=_("Greater than threshold or less"),
                                 choices=[('gt', _('greater')),
                                          ('lt', _('less'))])
    period = forms.IntegerField(label=_("Time"),
                                help_text=_("Time"))

    projects = forms.ChoiceField(label=_('Project'),
                                 widget=forms.Select(attrs={
                                       'class': 'switchable',
                                       'data-slug': 'project'}))

    def __init__(self, request, *args, **kwargs):
        super(AddAlarmForm, self).__init__(request, *args, **kwargs)

        data_handler = DataHandler()
        projects_choices = []
        vms_info = data_handler.instances_by_project()

        for project in vms_info:
            values = (project, _(project))
            projects_choices.append(values)

            data = 'data-project-' + project
            instances_choices = []
            sorted_vms_info_project = sorted(vms_info[project].items(), key=itemgetter(1))

            for instance in sorted_vms_info_project:
                values = (instance[0], _(vms_info[project][instance[0]]))
                instances_choices.append(values)

            self.fields[project] = forms.ChoiceField(choices=instances_choices,
                                                     widget=forms.SelectWidget(
                                                         attrs={'class': 'switched',
                                                         'data-switch-on': 'project',
                                                         data: _('Instances')}))

        choices = ([('all_projects', _("All Projects"))] + projects_choices)
        self.fields['projects'].choices = choices

        self.fields['send_mail'] = forms.BooleanField(label=
                                       _("Send the owner an email when the alarm is activated"),
                                       required=False)

    def handle(self, request, data):
        data_handler = DataHandler()
        project = data['projects']

        if(project != 'all_projects'):
            if(data_handler.add_alarm(data['name'], data['resource'],
                                      data['threshold'], data['operator'],
                                      data['period'], data['evalperiod'],
                                      data['send_mail'], data[project]) is not None):

                messages.success(request, _('Alarm has been created successfully.'))

                return True
        else:

            if(data_handler.add_alarm(data['name'], data['resource'],
                                      data['threshold'], data['operator'],
                                      data['period'], data['evalperiod'],
                                      data['send_mail']) is not None):

                messages.success(request, _('Alarm has been created successfully.'))

                return True

        return False

