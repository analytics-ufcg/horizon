# Copyright 2014 UFCG/Analytics.
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

from horizon import forms
from horizon import messages

from messages.message_selection import MessageManager


class MessageUserForm(forms.SelfHandlingForm):
    id = forms.CharField(label=_("ID"), widget=forms.HiddenInput)
    subject = forms.CharField(label=_("Subject"))
    message = forms.CharField(widget=forms.widgets.Textarea(),
                                  label=_("Message"))
    
    template = forms.ChoiceField(label=_("Templates"), help_text=_("Choose template"))
    instances = forms.ChoiceField(label=_("Instances"), help_text=_("Choose instance"), required=False) 
 
    def __init__(self, request, *args, **kwargs):
        super(MessageUserForm, self).__init__(request, *args, **kwargs)

        message_manager = MessageManager()

        #init template choices
        template_data = message_manager.get_templates()
        template_choices = []
        for key in template_data.keys():
            choice = (key, template_data[key]['name'])
            template_choices.append(choice)

        all_choices = ([('none', _("--Select Template--"))] + template_choices)
        self.fields['template'].choices = all_choices

        #init instances choices
        user_id = kwargs['initial'].get('id', None)
        instances_dict = message_manager.get_instances_dict(user_id)
        instances_choices = []
        for key in instances_dict.keys():
            choice = (key, instances_dict[key])
            instances_choices.append(choice)
        self.fields['instances'].choices = instances_choices

    def handle(self, request, data):
        message_manager = MessageManager();
        user_id = data.pop('id')

        try:
            url = ''
            if(str(data['template']) != 'none' and str(data['instances']) != ''):
                template_url = message_manager.get_action_url(data['template'])
                url = data['instances'] + '/' + template_url
            message_manager.send_message_user(data['subject'], data['message'], user_id, url)
            messages.success(request,
                             _('Message for User has been sent successfully.'))
        except Exception:
            messages.error(request, _('Unable to send message for the user.'))

        return True
    
    
class MessageProjectForm(forms.SelfHandlingForm):
    id = forms.CharField(label=_("ID"), widget=forms.HiddenInput)
    subject = forms.CharField(label=_("Subject"))
    message = forms.CharField(widget=forms.widgets.Textarea(),
                                  label=_("Message"))

    template = forms.ChoiceField(label=_("Templates"),
        help_text=_("Choose template"))

    def __init__(self, request, *args, **kwargs):
        super(MessageProjectForm, self).__init__(request, *args, **kwargs)

        message_manager = MessageManager()
        template_data = message_manager.get_templates()
        template_choices = []
        for key in template_data.keys():
            choice = (key, template_data[key]['name'])
            template_choices.append(choice)

        choices = ([('none', _("--Select Template--"))] + template_choices)
        self.fields['template'].choices = choices


    def handle(self, request, data):
        message_manager = MessageManager();
        project_id = data.pop('id')
        
        try:
            message_manager.send_message_project(data['subject'], data['message'], project_id, data['template'])
            messages.success(request,
                             _('Message for Project has been sent successfully.'))
        except Exception:
            messages.error(request, _('Unable to send message for the user.'))

        return True
        

class MessageHostForm(forms.SelfHandlingForm):
    id = forms.CharField(label=_("ID"), widget=forms.HiddenInput)
    subject = forms.CharField(label=_("Subject"))
    message = forms.CharField(widget=forms.widgets.Textarea(),
                                  label=_("Message"))

    template = forms.ChoiceField(label=_("Templates"),
        help_text=_("Choose template"))

    def __init__(self, request, *args, **kwargs):
        super(MessageHostForm, self).__init__(request, *args, **kwargs)

        message_manager = MessageManager()
        template_data = message_manager.get_templates()
        template_choices = []
        for key in template_data.keys():
            choice = (key, template_data[key]['name'])
            template_choices.append(choice)

        choices = ([('none', _("--Select Template--"))] + template_choices)
        self.fields['template'].choices = choices    


    def handle(self, request, data):
        message_manager = MessageManager();
        host_id = data.pop('id')
        
        try:
            message_manager.send_message_host(data['subject'], data['message'], host_id, data['template'])
            messages.success(request,
                             _('Message for Host has been sent successfully.'))
        except Exception:
            messages.error(request, _('Unable to send message for the user.'))

        return True
